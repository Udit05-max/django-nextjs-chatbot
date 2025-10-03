# /home/ram/aparsoft/backend/apps/accounts/models/custom_user.py

"""
Extended Django user model that supports role-based access (developer, client, project manager, 
admin), subscription tiers (standard to enterprise), and enhanced user management features 
including social auth, activity tracking, and role-specific profiles. Manages user 
permissions and access levels based on roles and subscription tiers, tailored for 
enterprise technology solution providers.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import transaction
from django.conf import settings
import logging
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.postgres.indexes import GinIndex
from typing import List, Dict, Any, Optional

from core.models import TimestampedModel, Country

from ..utils import helper, types
logger = logging.getLogger(__name__)


class CustomUser(AbstractUser):
    """Custom user model with additional fields and functionality tailored for technology solutions."""

    ROLE_CHOICES = [
        ('developer', 'Developer'),
        ('senior_developer', 'Senior Developer'),
        ('project_manager', 'Project Manager'),
        ('client', 'Client'),
        ('account_manager', 'Account Manager'),
        ('admin', 'Administrator'),
    ]

    SUBSCRIPTION_TIER_CHOICES = [
        ('standard', 'Standard'),
        ('professional', 'Professional'),
        ('business', 'Business'),
        ('enterprise', 'Enterprise')
    ]

    ROLE_STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('suspended', 'Suspended'),
        ('inactive', 'Inactive'),
        ('blocked', 'Blocked'),
    ]

    subscription_tier = models.CharField(
        max_length=20,
        choices=SUBSCRIPTION_TIER_CHOICES,
        default='standard'
    )

    # Core fields
    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_(
            'Primary email address used for account identification and communications')
    )

    # Role field
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='client',
        help_text=_('User role determines access and functionality')
    )
    role_status = models.CharField(
        max_length=40,
        choices=ROLE_STATUS_CHOICES,
        default='pending',
        help_text=_('Status of the user in their assigned role')
    )

    # Technical expertise and specialization
    technical_skills = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text=_('Technical skills and expertise levels')
    )

    specializations = models.JSONField(
        default=list,
        blank=True,
        null=True,
        help_text=_('Areas of specialization and expertise')
    )

    # Profile management
    profile_picture = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text=_('User profile picture/avatar')
    )

    # Verification and security
    email_verified = models.BooleanField(
        default=False,
        help_text=_('Indicates if the email address has been verified')
    )
    phone_verified = models.BooleanField(
        default=False,
        help_text=_('Indicates if the phone number has been verified')
    )
    two_factor_enabled = models.BooleanField(
        default=False,
        help_text=_('Indicates if two-factor authentication is enabled')
    )
    last_password_change = models.DateTimeField(
        auto_now_add=True,
        help_text=_('Timestamp of the last password change')
    )

    # Social auth
    social_auth_providers = models.JSONField(
        default=helper.get_default_social_auth_providers,
        help_text=_(
            'Connected social authentication providers and their associated data')
    )

    # Activity tracking
    last_active = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Timestamp of the user\'s last platform activity')
    )
    login_count = models.PositiveIntegerField(
        default=0,
        help_text=_('Number of times the user has logged in')
    )

    # Project and client relationship
    assigned_projects = models.ManyToManyField(
        'workitems.Project',
        blank=True,
        related_name='assigned_users',
        help_text=_('Projects the user is assigned to')
    )

    client_organization = models.ForeignKey(
        'customers.Organization',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='organization_users',
        help_text=_('Organization the user belongs to')
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']
        app_label = 'accounts'
        indexes = [
            models.Index(fields=['email'], name='user_email_idx'),
            models.Index(fields=['username'], name='user_username_idx'),
            models.Index(fields=['role'], name='user_role_idx'),
            models.Index(fields=['last_active'], name='user_last_active_idx'),
            models.Index(fields=['date_joined'], name='user_date_joined_idx'),
            models.Index(fields=['email_verified'],
                         name='user_email_verified_idx'),
            models.Index(fields=['email_verified', 'last_active'],
                         name='user_verified_active_idx'),
            # Add GIN index for JSON fields
            GinIndex(fields=['social_auth_providers'],
                     name='user_social_auth_gin_idx'),
            GinIndex(fields=['technical_skills'],
                     name='user_tech_skills_gin_idx'),
            GinIndex(fields=['specializations'],
                     name='user_specializations_gin_idx'),
        ]

    def __str__(self) -> str:
        return self.email

    @property
    def full_name(self) -> str:
        """Return user's full name or username."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    @property
    def account_age_days(self) -> int:
        """Get account age in days."""
        return (timezone.now() - self.date_joined).days

    @property
    def is_developer(self) -> bool:
        """Check if user is a developer."""
        return self.role == 'developer'

    @property
    def is_senior_developer(self) -> bool:
        """Check if user is a senior developer."""
        return self.role == 'senior_developer'

    @property
    def is_project_manager(self) -> bool:
        """Check if user is a project manager."""
        return self.role == 'project_manager'

    @property
    def is_client(self) -> bool:
        """Check if user is a client."""
        return self.role == 'client'

    @property
    def is_account_manager(self) -> bool:
        """Check if user is an account manager."""
        return self.role == 'account_manager'

    @property
    def is_professional(self) -> bool:
        """Check if user has professional tier."""
        return self.subscription_tier in ['professional', 'business', 'enterprise']

    @property
    def is_business(self) -> bool:
        """Check if user has business tier."""
        return self.subscription_tier in ['business', 'enterprise']

    @property
    def is_enterprise(self) -> bool:
        """Check if user has enterprise tier."""
        return self.subscription_tier == 'enterprise'

    @property
    def can_access_advanced_features(self) -> bool:
        """Check if user can access advanced features."""
        return (self.role in ['developer', 'senior_developer', 'project_manager', 'admin'] and
                self.subscription_tier in ['professional', 'business', 'enterprise'])

    @property
    def can_manage_projects(self) -> bool:
        """Check if user can manage projects."""
        return self.role in ['project_manager', 'admin', 'account_manager']

    @property
    def can_access_analytics(self) -> bool:
        """Check if user can access analytics."""
        return self.role in ['project_manager', 'admin', 'account_manager'] or self.is_enterprise

    def update_subscription(self, new_tier: str, reason: str = None) -> bool:
        """
        Update user's subscription tier with validation and proper cascading updates.

        Args:
            new_tier: The new subscription tier to set
            reason: Optional reason for the change

        Returns:
            bool: Success status of the update
        """
        if new_tier not in dict(self.SUBSCRIPTION_TIER_CHOICES):
            raise ValueError(f"Invalid subscription tier: {new_tier}")

        try:
            with transaction.atomic():
                old_tier = self.subscription_tier
                self.subscription_tier = new_tier

                # Update related profile quotas and permissions
                if self.role == 'developer' and hasattr(self, 'developer_profile'):
                    self._update_developer_permissions(old_tier, new_tier)
                elif self.role == 'client' and hasattr(self, 'client_profile'):
                    self._update_client_permissions(old_tier, new_tier)
                elif self.role == 'project_manager' and hasattr(self, 'project_manager_profile'):
                    self._update_project_manager_permissions(
                        old_tier, new_tier)

                self.save()

                # Log subscription change
                logger.info(
                    f"Subscription updated for user {self.email} from {old_tier} to {new_tier}. "
                    f"Reason: {reason or 'Not specified'}"
                )
                return True

        except Exception as e:
            logger.error(
                f"Error updating subscription for user {self.email}: {str(e)}")
            raise

    def _update_developer_permissions(self, old_tier: str, new_tier: str) -> None:
        """Update developer permissions based on subscription change."""
        developer = self.developer_profile

        # Define tier-based resource limits
        tier_limits = {
            'standard': {'resource_limit': 50, 'advanced_tools_access': False},
            'professional': {'resource_limit': 200, 'advanced_tools_access': True},
            'business': {'resource_limit': 500, 'advanced_tools_access': True},
            'enterprise': {'resource_limit': None, 'advanced_tools_access': True}
        }

        # Update developer's settings
        if not developer.resource_allocation:
            developer.resource_allocation = {}

        developer.resource_allocation.update({
            'monthly_limit': tier_limits[new_tier]['resource_limit'],
            'advanced_tools_access': tier_limits[new_tier]['advanced_tools_access'],
            'last_updated': timezone.now().isoformat()
        })

        developer.save(update_fields=['resource_allocation'])

    def _update_client_permissions(self, old_tier: str, new_tier: str) -> None:
        """Update client permissions based on subscription change."""
        client = self.client_profile

        # Define tier-based access levels
        tier_access = {
            'standard': {
                'project_reports_access': False,
                'api_tokens': 3,
                'custom_integrations': False,
                'support_level': 'basic'
            },
            'professional': {
                'project_reports_access': True,
                'api_tokens': 10,
                'custom_integrations': False,
                'support_level': 'standard'
            },
            'business': {
                'project_reports_access': True,
                'api_tokens': 25,
                'custom_integrations': True,
                'support_level': 'priority'
            },
            'enterprise': {
                'project_reports_access': True,
                'api_tokens': None,  # Unlimited
                'custom_integrations': True,
                'support_level': 'dedicated'
            }
        }

        # Update client's access levels
        if not client.access_levels:
            client.access_levels = {}

        client.access_levels.update({
            'subscription_features': tier_access[new_tier],
            'last_tier_update': timezone.now().isoformat()
        })

        client.save(update_fields=['access_levels'])

    def _update_project_manager_permissions(self, old_tier: str, new_tier: str) -> None:
        """Update project manager permissions based on subscription change."""
        pm = self.project_manager_profile

        # Define tier-based project quotas
        tier_quotas = {
            'professional': {
                'max_projects': 5,
                'team_members': 10,
                'analytics_level': 'basic'
            },
            'business': {
                'max_projects': 15,
                'team_members': 25,
                'analytics_level': 'advanced'
            },
            'enterprise': {
                'max_projects': None,  # Unlimited
                'team_members': None,  # Unlimited
                'analytics_level': 'premium'
            }
        }

        # Update quotas
        if new_tier in tier_quotas:
            if not pm.project_quotas:
                pm.project_quotas = {}

            pm.project_quotas.update({
                'limits': tier_quotas[new_tier],
                'reset_date': (timezone.now() + timezone.timedelta(days=30)).isoformat()
            })

            pm.save(update_fields=['project_quotas'])

    def get_role_profile(self):
        """Get the user's role-specific profile."""
        if self.role == 'developer' or self.role == 'senior_developer':
            return getattr(self, 'developer_profile', None)
        elif self.role == 'project_manager':
            return getattr(self, 'project_manager_profile', None)
        elif self.role == 'client':
            return getattr(self, 'client_profile', None)
        elif self.role == 'account_manager':
            return getattr(self, 'account_manager_profile', None)
        return None

    def get_profile(self):
        """Get the user's profile based on their role."""
        return self.get_role_profile()

    def get_assigned_projects(self) -> List[Dict[str, Any]]:
        """Get all projects the user is assigned to with enhanced details."""
        projects = self.assigned_projects.all().select_related('client')

        return [{
            'project': project,
            'role': project.get_user_role(self),
            'status': project.status,
            'client': project.client,
            'start_date': project.start_date,
            'deadline': project.deadline,
            'tasks_count': project.get_user_tasks_count(self),
            'completed_tasks': project.get_user_completed_tasks_count(self)
        } for project in projects]

    def update_last_active(self, save: bool = True) -> None:
        """Update user's last active timestamp."""
        self.last_active = timezone.now()
        if save:
            self.save(update_fields=['last_active'])

    def verify_email(self) -> bool:
        """Verify user's email address."""
        if not self.email_verified:
            self.email_verified = True
            self.save(update_fields=['email_verified'])
            return True
        return False

    def add_social_auth_provider(self, provider: str, connection_data: dict) -> bool:
        """Add or update a social authentication provider."""
        if not self.social_auth_providers:
            self.social_auth_providers = helper.get_default_social_auth_providers()

        provider_data = types.SocialAuthConnection(**connection_data)
        self.social_auth_providers['connections'][provider] = provider_data
        if provider not in self.social_auth_providers['active_providers']:
            self.social_auth_providers['active_providers'].append(provider)

        self.save(update_fields=['social_auth_providers'])
        return True

    def remove_social_auth_provider(self, provider: str) -> bool:
        """Remove a social authentication provider."""
        if (self.social_auth_providers and
                provider in self.social_auth_providers['connections']):
            del self.social_auth_providers['connections'][provider]
            if provider in self.social_auth_providers['active_providers']:
                self.social_auth_providers['active_providers'].remove(provider)
            if self.social_auth_providers['default_login'] == provider:
                self.social_auth_providers['default_login'] = None
            self.save(update_fields=['social_auth_providers'])
            return True
        return False

    def get_login_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get user's recent login history."""
        # Assuming you have a separate LoginHistory model
        return (self.login_history.all()
                .select_related('device')
                .order_by('-created_at')[:limit]
                .values('id', 'ip_address', 'device__name', 'created_at'))

    def add_technical_skill(self, skill: str, level: str) -> bool:
        """Add or update a technical skill for the user."""
        if not self.technical_skills:
            self.technical_skills = {}

        self.technical_skills[skill] = level
        self.save(update_fields=['technical_skills'])
        return True

    def add_specialization(self, specialization: str) -> bool:
        """Add a specialization for the user."""
        if not self.specializations:
            self.specializations = []

        if specialization not in self.specializations:
            self.specializations.append(specialization)
            self.save(update_fields=['specializations'])
            return True
        return False

    def get_technical_skills(self) -> Dict[str, str]:
        """Get user's technical skills."""
        return self.technical_skills or {}

    def get_specializations(self) -> List[str]:
        """Get user's specializations."""
        return self.specializations or []


class UserContact(TimestampedModel):
    """User contact information."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contact'
    )
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_DEFAULT,
        default=1,
        null=True,
        help_text=_('Country of residence')
    )
    contact_info = models.JSONField(
        default=helper.get_default_user_contact_info,
        null=True,
        blank=True,
        help_text=_(
            'Structured contact information including phones and social profiles')
    )
    billing_details = models.JSONField(
        default=dict,
        null=True,
        blank=True,
        help_text=_('Billing information for invoicing')
    )

    timezone = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_('User timezone for project coordination')
    )

    availability = models.JSONField(
        default=dict,
        null=True,
        blank=True,
        help_text=_('User availability schedule')
    )

    class Meta:
        indexes = [
            models.Index(fields=['user'], name='user_contact_user_idx'),
            GinIndex(fields=['contact_info'],
                     name='user_contact_info_gin_idx'),
            GinIndex(fields=['billing_details'],
                     name='user_billing_gin_idx'),
            GinIndex(fields=['availability'],
                     name='user_availability_gin_idx'),
        ]

    def __str__(self) -> str:
        return f"Contact for {self.user.email}"
