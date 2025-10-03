"""
Django admin configuration for CustomUser and UserContact models.
Provides comprehensive admin interface for user management with proper
organization of fields, filters, and search capabilities.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.forms import Textarea
import json

from ..models.custom_user import CustomUser, UserContact


class UserContactInline(admin.StackedInline):
    """Inline admin for UserContact model."""

    model = UserContact
    extra = 0
    can_delete = False

    fieldsets = (
        (
            _("Address Information"),
            {
                "fields": (
                    "address_line1",
                    "address_line2",
                    "city",
                    "state",
                    "postal_code",
                    "country",
                    "timezone",
                )
            },
        ),
        (
            _("Contact Details"),
            {
                "fields": ("contact_info",),
                "classes": ("collapse",),
            },
        ),
        (
            _("Billing & Availability"),
            {
                "fields": ("billing_details", "availability"),
                "classes": ("collapse",),
            },
        ),
    )

    formfield_overrides = {
        models.JSONField: {"widget": Textarea(attrs={"rows": 4, "cols": 80})},
    }


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Admin configuration for CustomUser model."""

    inlines = [UserContactInline]

    # List display configuration
    list_display = (
        "email",
        "username",
        "get_full_name_display",
        "role",
        "subscription_tier",
        "role_status",
        "email_verified",
        "is_active",
        "last_active",
        "date_joined",
        "get_profile_link",
    )

    list_display_links = ("email", "username")

    # List filters
    list_filter = (
        "role",
        "subscription_tier",
        "role_status",
        "email_verified",
        "phone_verified",
        "two_factor_enabled",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
        "last_active",
    )

    # Search fields
    search_fields = (
        "email",
        "username",
        "first_name",
        "last_name",
        "client_organization__name",
    )

    # Ordering
    ordering = ("-date_joined",)

    # Date hierarchy
    date_hierarchy = "date_joined"

    # Readonly fields
    readonly_fields = (
        "account_age_days",
        "last_password_change",
        "date_joined",
        "last_login",
        "login_count",
        "get_profile_link",
        "get_assigned_projects_count",
    )

    # Fieldset organization
    fieldsets = (
        (
            _("Basic Information"),
            {
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "password",
                )
            },
        ),
        (
            _("Role & Permissions"),
            {
                "fields": (
                    "role",
                    "role_status",
                    "subscription_tier",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Verification & Security"),
            {
                "fields": (
                    "email_verified",
                    "phone_verified",
                    "two_factor_enabled",
                    "last_password_change",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Technical Skills"),
            {
                "fields": (
                    "technical_skills",
                    "specializations",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Social Authentication"),
            {
                "fields": ("social_auth_providers",),
                "classes": ("collapse",),
            },
        ),
        (
            _("Activity & Engagement"),
            {
                "fields": (
                    "last_active",
                    "login_count",
                    "date_joined",
                    "last_login",
                    "account_age_days",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Project & Organization"),
            {
                "fields": (
                    "client_organization",
                    "assigned_projects",
                    "get_assigned_projects_count",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Profile Links"),
            {
                "fields": ("get_profile_link",),
                "classes": ("collapse",),
            },
        ),
    )

    # Add fieldsets for creating new users
    add_fieldsets = (
        (
            _("Essential Information"),
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                ),
            },
        ),
        (
            _("Role Assignment"),
            {
                "classes": ("wide",),
                "fields": (
                    "role",
                    "subscription_tier",
                    "role_status",
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "classes": ("wide",),
                "fields": (
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )

    # Custom form overrides for better JSON field display
    formfield_overrides = {
        models.JSONField: {"widget": Textarea(attrs={"rows": 4, "cols": 80})},
    }

    # Filter horizontal for many-to-many fields
    filter_horizontal = ("groups", "user_permissions", "assigned_projects")

    # Actions
    actions = [
        "activate_users",
        "deactivate_users",
        "verify_emails",
        "approve_role_status",
        "upgrade_to_professional",
        "upgrade_to_business",
        "upgrade_to_enterprise",
    ]

    def get_full_name_display(self, obj):
        """Display full name with fallback to username."""
        return obj.full_name

    get_full_name_display.short_description = _("Full Name")

    def get_profile_link(self, obj):
        """Generate links to role-specific profiles."""
        profile = obj.get_role_profile()
        if not profile:
            return _("No profile")

        if obj.role in ["developer", "senior_developer"]:
            url = reverse("admin:accounts_developerprofile_change", args=[profile.id])
            return format_html('<a href="{}">View Developer Profile</a>', url)
        elif obj.role == "client":
            url = reverse("admin:accounts_clientprofile_change", args=[profile.id])
            return format_html('<a href="{}">View Client Profile</a>', url)
        # Add other role profile links as needed

        return _("View Profile")

    get_profile_link.short_description = _("Profile")

    def get_assigned_projects_count(self, obj):
        """Get count of assigned projects."""
        return obj.assigned_projects.count()

    get_assigned_projects_count.short_description = _("Assigned Projects")

    def account_age_days(self, obj):
        """Display account age in days."""
        return f"{obj.account_age_days} days"

    account_age_days.short_description = _("Account Age")

    # Custom admin actions
    def activate_users(self, request, queryset):
        """Activate selected users."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} user(s) were successfully activated.")

    activate_users.short_description = _("Activate selected users")

    def deactivate_users(self, request, queryset):
        """Deactivate selected users."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} user(s) were successfully deactivated.")

    deactivate_users.short_description = _("Deactivate selected users")

    def verify_emails(self, request, queryset):
        """Mark emails as verified."""
        updated = queryset.update(email_verified=True)
        self.message_user(
            request, f"{updated} user email(s) were successfully verified."
        )

    verify_emails.short_description = _("Verify user emails")

    def approve_role_status(self, request, queryset):
        """Approve pending role status."""
        updated = queryset.filter(role_status="pending").update(role_status="approved")
        self.message_user(
            request, f"{updated} user role(s) were successfully approved."
        )

    approve_role_status.short_description = _("Approve pending role status")

    def upgrade_to_professional(self, request, queryset):
        """Upgrade to professional tier."""
        updated = queryset.update(subscription_tier="professional")
        self.message_user(request, f"{updated} user(s) upgraded to Professional tier.")

    upgrade_to_professional.short_description = _("Upgrade to Professional")

    def upgrade_to_business(self, request, queryset):
        """Upgrade to business tier."""
        updated = queryset.update(subscription_tier="business")
        self.message_user(request, f"{updated} user(s) upgraded to Business tier.")

    upgrade_to_business.short_description = _("Upgrade to Business")

    def upgrade_to_enterprise(self, request, queryset):
        """Upgrade to enterprise tier."""
        updated = queryset.update(subscription_tier="enterprise")
        self.message_user(request, f"{updated} user(s) upgraded to Enterprise tier.")

    upgrade_to_enterprise.short_description = _("Upgrade to Enterprise")


@admin.register(UserContact)
class UserContactAdmin(admin.ModelAdmin):
    """Admin configuration for UserContact model."""

    list_display = (
        "user",
        "get_user_email",
        "city",
        "state",
        "country",
        "timezone",
        "created_at",
    )

    list_filter = (
        "country",
        "timezone",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "city",
        "state",
        "address_line1",
    )

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (_("User"), {"fields": ("user",)}),
        (
            _("Address"),
            {
                "fields": (
                    "address_line1",
                    "address_line2",
                    "city",
                    "state",
                    "postal_code",
                    "country",
                    "timezone",
                )
            },
        ),
        (
            _("Contact Information"),
            {
                "fields": ("contact_info",),
                "classes": ("collapse",),
            },
        ),
        (
            _("Billing Details"),
            {
                "fields": ("billing_details",),
                "classes": ("collapse",),
            },
        ),
        (
            _("Availability"),
            {
                "fields": ("availability",),
                "classes": ("collapse",),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    formfield_overrides = {
        models.JSONField: {"widget": Textarea(attrs={"rows": 4, "cols": 80})},
    }

    def get_user_email(self, obj):
        """Display user email."""
        return obj.user.email

    get_user_email.short_description = _("Email")
    get_user_email.admin_order_field = "user__email"
