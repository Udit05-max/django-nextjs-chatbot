# /home/ram/aparsoft/backend/apps/accounts/signals/user_creation_signals.py

"""
User Creation and Profile Management Signals Module

This module manages automated profile creation and role management for the Aparsoft platform.

Key functionalities:
- Automatic profile creation for new users based on their role (Developer/Client/Project Manager/Account Manager)
- Role-based access control and subscription management
- Role change management with proper profile cleanup
- Profile status synchronization
- Organization user management

Signal Flow:
1. New User Created → Creates appropriate profile(s) with initial subscription tier
2. Role Change → Cleans up old profiles and creates new ones
3. User Creation/Deletion → Updates organization user counts
4. Profile Status Updates → Synchronizes user role status
"""

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.db import transaction, IntegrityError
from django.utils import timezone

from ..models import (
    CustomUser,
    DeveloperProfile,
    ClientProfile,
    ProjectManagerProfile,
    AccountManagerProfile,
    UserContact,
)
from core.models import Country

import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create appropriate profile based on user role.
    Handles creation of Developer, Client, Project Manager, or Account Manager profiles.
    Sets initial subscription tier and status.
    """
    if created:
        try:
            with transaction.atomic():
                # Create contact info for all user types
                try:
                    # Try to get a default country (create one if none exists)
                    default_country = None
                    try:
                        # Try to get any active country, preferably India or USA
                        default_country = Country.objects.filter(is_active=True).first()
                        if not default_country:
                            # Create a default country if none exists
                            default_country = Country.objects.create(
                                name="India",
                                code="IN",
                                phone_code="+91",
                                is_active=True,
                            )
                            logger.info("Created default country (India)")
                    except Exception as e:
                        logger.warning(
                            f"Could not create/get default country: {str(e)}"
                        )
                        default_country = None

                    UserContact.objects.create(
                        user=instance,
                        contact_info={},  # Will use default from helper
                        country=default_country,
                    )
                    logger.info(f"Created user contact for {instance.email}")
                except IntegrityError:
                    logger.warning(
                        f"Contact information already exists for user {instance.email}. Skipping creation."
                    )
                except Exception as e:
                    logger.error(
                        f"Error creating user contact for {instance.email}: {str(e)}"
                    )

                if instance.role == "developer" or instance.role == "senior_developer":
                    # Safety check to prevent duplicates
                    if not hasattr(instance, "developer_profile"):
                        # Create developer profile
                        DeveloperProfile.objects.create(
                            user=instance,
                            experience_level="mid",  # Default experience level
                            employment_type="full_time",  # Default employment type
                            headline=f"{instance.role.replace('_', ' ').title()} at Aparsoft",
                            technical_expertise=[],  # Empty list, to be filled later
                            professional_info={},  # Will use default from helper
                            availability={},  # Will use default from helper
                            utilization_rate=0.0,  # Default utilization
                        )
                        logger.info(f"Created developer profile for {instance.email}")
                    else:
                        logger.warning(
                            f"Developer profile already exists for {instance.email}"
                        )

                    # Set role status to approved for immediate access
                    CustomUser.objects.filter(pk=instance.pk).update(
                        role_status="approved"
                    )

                elif instance.role == "client":
                    # Create client profile with active status for immediate access
                    if not hasattr(instance, "client_profile"):
                        ClientProfile.objects.create(
                            user=instance,
                            client_type="individual",  # Default client type
                            client_status="active",  # Active status for immediate access
                            industry_sector="technology",  # Default sector
                        )
                        logger.info(
                            f"Created client profile with active status for {instance.email}"
                        )
                    else:
                        logger.warning(
                            f"Client profile already exists for {instance.email}"
                        )

                    # Set role status to approved for immediate access
                    CustomUser.objects.filter(pk=instance.pk).update(
                        role_status="approved"
                    )

                elif instance.role == "project_manager":
                    # Create project manager profile with active status
                    if not hasattr(instance, "project_manager_profile"):
                        ProjectManagerProfile.objects.create(
                            user=instance,
                            experience_level="intermediate",  # Default experience
                            primary_methodology="agile",  # Default methodology
                            headline="Project Manager at Aparsoft",
                            certifications=[],  # Empty list, to be filled later
                            professional_info={},  # Will use default from helper
                            project_history={},  # Will use default from helper
                        )
                        logger.info(
                            f"Created project manager profile for {instance.email}"
                        )
                    else:
                        logger.warning(
                            f"Project manager profile already exists for {instance.email}"
                        )

                    # Set role status to approved for immediate access
                    CustomUser.objects.filter(pk=instance.pk).update(
                        role_status="approved"
                    )

                elif instance.role == "account_manager":
                    # Create account manager profile with active status
                    if not hasattr(instance, "account_manager_profile"):
                        AccountManagerProfile.objects.create(
                            user=instance,
                            experience_level="mid",  # Default experience
                            sales_focus="account_growth",  # Default sales focus
                            headline="Account Manager at Aparsoft",
                            certifications=[],  # Empty list, to be filled later
                            professional_info={},  # Will use default from helper
                            client_portfolio={},  # Will use default from helper
                            active_clients_count=0,  # No clients initially
                            client_satisfaction_score=0.0,  # Default score
                        )
                        logger.info(
                            f"Created account manager profile for {instance.email}"
                        )
                    else:
                        logger.warning(
                            f"Account manager profile already exists for {instance.email}"
                        )

                    # Set role status to approved for immediate access
                    CustomUser.objects.filter(pk=instance.pk).update(
                        role_status="approved"
                    )

                elif instance.role == "admin":
                    # Admins don't need specific profiles
                    CustomUser.objects.filter(pk=instance.pk).update(
                        role_status="approved"
                    )
                    logger.info(f"Set admin status for {instance.email}")

                logger.info(
                    f"Created profile for user {instance.email} with role {instance.role}"
                )

        except IntegrityError as e:
            # Handle specific database integrity errors
            if "violates foreign key constraint" in str(e):
                logger.error(
                    f"Foreign key constraint error for user {instance.email}: {str(e)}"
                )
            else:
                logger.error(
                    f"Database integrity error creating profile for user {instance.email}: {str(e)}"
                )
        except Exception as e:
            logger.error(
                f"Error creating profile for user {instance.email}: {str(e)}",
                exc_info=True,
            )


@receiver(pre_save, sender=CustomUser)
def handle_role_change(sender, instance, **kwargs):
    """
    Signal to handle role changes and ensure profile consistency.
    Creates new profile after cleaning up old ones.
    """
    # Skip for new users
    if not instance.pk:
        return

    # Prevent recursion
    if getattr(instance, "_handling_role_change", False):
        return

    # Get the current role directly from the database
    try:
        current_db_role = CustomUser.objects.filter(pk=instance.pk).values_list(
            "role", flat=True
        )[0]
    except (IndexError, Exception) as e:
        logger.error(f"Error getting current role from database: {str(e)}")
        return

    # Only proceed if the role has actually changed
    if current_db_role != instance.role:
        try:
            # Set flag to prevent recursion
            instance._handling_role_change = True

            # Store the new role value to ensure it doesn't get lost
            new_role = instance.role

            logger.info(
                f"Role change detected for {instance.email}: {current_db_role} → {new_role}"
            )

            with transaction.atomic():
                # Clean up existing profiles
                try:
                    if hasattr(instance, "developer_profile"):
                        instance.developer_profile.delete()
                        logger.info(
                            f"Deleted developer profile for user {instance.email}"
                        )

                    if hasattr(instance, "client_profile"):
                        instance.client_profile.delete()
                        logger.info(f"Deleted client profile for user {instance.email}")

                    if hasattr(instance, "project_manager_profile"):
                        instance.project_manager_profile.delete()
                        logger.info(
                            f"Deleted project manager profile for user {instance.email}"
                        )

                    if hasattr(instance, "account_manager_profile"):
                        instance.account_manager_profile.delete()
                        logger.info(
                            f"Deleted account manager profile for user {instance.email}"
                        )
                except Exception as e:
                    logger.error(
                        f"Error cleaning up profiles for {instance.email}: {str(e)}"
                    )

                # Make sure role stays correct - this is critical
                instance.role = new_role

                # Update role directly in DB to ensure persistence
                CustomUser.objects.filter(pk=instance.pk).update(role=new_role)

                # Create new profile based on the new role
                if new_role in ["developer", "senior_developer"]:
                    DeveloperProfile.objects.create(
                        user=instance,
                        experience_level="mid",
                        employment_type="full_time",
                        headline=f"{new_role.replace('_', ' ').title()} at Aparsoft",
                        technical_expertise=[],
                        professional_info={},
                        availability={},
                        utilization_rate=0.0,
                    )
                    CustomUser.objects.filter(pk=instance.pk).update(
                        role_status="approved"
                    )
                    logger.info(f"Created developer profile for {instance.email}")

                elif new_role == "client":
                    ClientProfile.objects.create(
                        user=instance,
                        client_type="individual",
                        client_status="active",  # Active status for immediate access
                        industry_sector="technology",
                    )
                    CustomUser.objects.filter(pk=instance.pk).update(
                        role_status="approved"
                    )
                    logger.info(
                        f"Created client profile with active status for {instance.email}"
                    )

                elif new_role == "project_manager":
                    ProjectManagerProfile.objects.create(
                        user=instance,
                        experience_level="intermediate",
                        primary_methodology="agile",
                        headline="Project Manager at Aparsoft",
                        certifications=[],
                        professional_info={},
                        project_history={},
                    )
                    CustomUser.objects.filter(pk=instance.pk).update(
                        role_status="approved"
                    )
                    logger.info(f"Created project manager profile for {instance.email}")

                elif new_role == "account_manager":
                    AccountManagerProfile.objects.create(
                        user=instance,
                        experience_level="mid",
                        sales_focus="account_growth",
                        headline="Account Manager at Aparsoft",
                        certifications=[],
                        professional_info={},
                        client_portfolio={},
                        active_clients_count=0,
                        client_satisfaction_score=0.0,
                    )
                    CustomUser.objects.filter(pk=instance.pk).update(
                        role_status="approved"
                    )
                    logger.info(f"Created account manager profile for {instance.email}")

                elif new_role == "admin":
                    # Admins don't need specific profiles
                    CustomUser.objects.filter(pk=instance.pk).update(
                        role_status="approved"
                    )
                    logger.info(f"Set admin status for {instance.email}")

                # Final persistence check - make absolutely sure the role is saved
                CustomUser.objects.filter(pk=instance.pk).update(role=new_role)

                logger.info(
                    f"Role change completed for user {instance.email}: {current_db_role} → {new_role}"
                )

        except Exception as e:
            logger.error(
                f"Error handling role change for user {instance.email}: {str(e)}",
                exc_info=True,
            )
        finally:
            # Clear the flag to allow future role changes
            if hasattr(instance, "_handling_role_change"):
                del instance._handling_role_change


@receiver(post_save, sender=DeveloperProfile)
def handle_developer_status_change(sender, instance, created, **kwargs):
    """
    Signal to handle developer status changes.
    """
    if not created:
        try:
            user = instance.user
            # Sync user role status with profile status
            if instance.status == "active":
                CustomUser.objects.filter(pk=user.pk).update(role_status="approved")
            elif instance.status == "inactive":
                CustomUser.objects.filter(pk=user.pk).update(role_status="inactive")
            logger.info(f"Updated role status for developer {user.email}")
        except Exception as e:
            logger.error(f"Error handling developer status change: {str(e)}")


@receiver(post_save, sender=ClientProfile)
def handle_client_status_change(sender, instance, created, **kwargs):
    """
    Signal to handle client status changes.
    """
    if not created:
        try:
            user = instance.user
            # Sync user role status with client status
            if instance.client_status == "active":
                CustomUser.objects.filter(pk=user.pk).update(role_status="approved")
            elif instance.client_status == "inactive":
                CustomUser.objects.filter(pk=user.pk).update(role_status="inactive")
            elif instance.client_status == "suspended":
                CustomUser.objects.filter(pk=user.pk).update(role_status="suspended")
            logger.info(f"Updated role status for client {user.email}")
        except Exception as e:
            logger.error(f"Error handling client status change: {str(e)}")


@receiver(post_save, sender=ProjectManagerProfile)
def handle_project_manager_status_change(sender, instance, created, **kwargs):
    """
    Signal to handle project manager status changes.
    """
    if not created:
        try:
            user = instance.user
            # Sync user role status with project manager status
            if instance.status == "active":
                CustomUser.objects.filter(pk=user.pk).update(role_status="approved")
            elif instance.status == "inactive":
                CustomUser.objects.filter(pk=user.pk).update(role_status="inactive")
            logger.info(f"Updated role status for project manager {user.email}")
        except Exception as e:
            logger.error(f"Error handling project manager status change: {str(e)}")


@receiver(post_save, sender=AccountManagerProfile)
def handle_account_manager_status_change(sender, instance, created, **kwargs):
    """
    Signal to handle account manager status changes.
    """
    if not created:
        try:
            user = instance.user
            # Sync user role status with account manager status
            if instance.status == "active":
                CustomUser.objects.filter(pk=user.pk).update(role_status="approved")
            elif instance.status == "inactive":
                CustomUser.objects.filter(pk=user.pk).update(role_status="inactive")
            logger.info(f"Updated role status for account manager {user.email}")
        except Exception as e:
            logger.error(f"Error handling account manager status change: {str(e)}")


@receiver(post_save, sender=CustomUser)
def update_organization_user_counts(sender, instance, created, **kwargs):
    """Update organization counts when users are created"""
    if instance.client_organization and created:
        if instance.role == "client":
            # Update client count in organization if needed
            pass
        # Add other role-based organization count updates as needed
        logger.info(f"Updated organization counts for user {instance.email}")


@receiver(post_delete, sender=CustomUser)
def decrease_organization_user_counts(sender, instance, **kwargs):
    """Decrease organization counts when users are deleted"""
    if instance.client_organization:
        if instance.role == "client":
            # Decrease client count in organization if needed
            pass
        # Add other role-based organization count decreases as needed
        logger.info(f"Decreased organization counts for deleted user {instance.email}")
