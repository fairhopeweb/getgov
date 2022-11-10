"""Forms Wizard for creating a new domain application."""

import logging

from django import forms

from django.contrib.auth.mixins import LoginRequiredMixin

from formtools.wizard.views import NamedUrlSessionWizardView  # type: ignore


logger = logging.getLogger(__name__)

class RegistrarForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(RegistrarForm, self).__init__(*args, **kwargs)

class OrganizationForm(RegistrarForm):
    organization_type = forms.ChoiceField(
        required=True,
        choices=[
            ("Federal", "Federal: a federal agency"),
            ("Interstate", "Interstate: an organization of two or more states"),
            (
                "State_or_Territory",
                (
                    "State or Territory: One of the 50 U.S. states, the District of "
                    "Columbia, American Samoa, Guam, Northern Mariana Islands, "
                    "Puerto Rico, or the U.S. Virgin Islands"
                ),
            ),
            (
                "Tribal",
                (
                    "Tribal: a tribal government recognized by the federal or "
                    "state government"
                ),
            ),
            ("County", "County: a county, parish, or borough"),
            ("City", "City: a city, town, township, village, etc."),
            (
                "Special_District",
                "Special District: an independent organization within a single state",
            ),
        ],
        widget=forms.RadioSelect,
    )
    federal_type = forms.ChoiceField(
        required=False,
        choices=[
            ("Executive", "Executive"),
            ("Judicial", "Judicial"),
            ("Legislative", "Legislative"),
        ],
        widget=forms.RadioSelect,
    )
    is_election_board = forms.ChoiceField(
        required=False,
        choices=[
            ("Yes", "Yes"),
            ("No", "No"),
        ],
        widget=forms.RadioSelect(attrs={"class":"usa-radio__input"}),
    )

class OrganizationFederalForm(RegistrarForm):
    federal_type = forms.ChoiceField(
        required=False,
        choices=[
            ("Executive", "Executive"),
            ("Judicial", "Judicial"),
            ("Legislative", "Legislative"),
        ],
        widget=forms.RadioSelect,
    )

class OrganizationElectionForm(RegistrarForm):
    is_election_board = forms.ChoiceField(
        required=False,
        choices=[
            ("Yes", "Yes"),
            ("No", "No"),
        ],
        widget=forms.RadioSelect(),
    )

class OrgContactForm(RegistrarForm):
    organization_name = forms.CharField(label="Organization Name")
    address_line1 = forms.CharField(label="Address line 1")
    address_line2 = forms.CharField(
            required=False,
            label="Address line 2",
            )
    us_state = forms.ChoiceField(
            label="State",
            choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'), ('AS', 'American Samoa'), ('GU', 'Guam'), ('MP', 'Northern Mariana Islands'), ('PR', 'Puerto Rico'), ('VI', 'Virgin Islands'),],
            )
    zipcode = forms.CharField(label="ZIP code")

class AuthorizingOfficialForm(RegistrarForm):
    given_name = forms.CharField(label="First name/given name")
    middle_name = forms.CharField(
            required=False,
            label="Middle name (optional)",
            )
    family_name = forms.CharField(label="Last name/family name")
    title = forms.CharField(label="Title or role in your organization")
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Phone")

class CurrentSitesForm(RegistrarForm):
    current_site = forms.CharField(
            required=False,
            label="Enter your organization’s public website, if you have one. For example, www.city.com.")

class DotGovDomainForm(RegistrarForm):
    dotgov_domain = forms.CharField(label="What .gov domain do you want?")
    alternative_domain = forms.CharField(
            required = False,
            label="Are there other domains you’d like if we can’t give you your first choice? Entering alternative domains is optional.",
            )

class PurposeForm(RegistrarForm):
    purpose_field = forms.CharField(label="Purpose", widget=forms.Textarea())

class YourContactForm(RegistrarForm):
    given_name = forms.CharField(label="First name/given name")
    middle_name = forms.CharField(
            required=False,
            label="Middle name (optional)",
            )
    family_name = forms.CharField(label="Last name/family name")
    title = forms.CharField(label="Title or role in your organization")
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Phone")

class OtherContactsForm(RegistrarForm):
    given_name = forms.CharField(label="First name/given name")
    middle_name = forms.CharField(
            required=False,
            label="Middle name (optional)",
            )
    family_name = forms.CharField(label="Last name/family name")
    title = forms.CharField(label="Title or role in your organization")
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Phone")

class SecurityEmailForm(RegistrarForm):
    email = forms.EmailField(
            required=False,
            label="Security email",
            )

class AnythingElseForm(RegistrarForm):
    anything_else = forms.CharField(
            required=False,
            label="Anything else we should know", 
            widget=forms.Textarea()
            )

class RequirementsForm(RegistrarForm):
    agree_check = forms.BooleanField(label="I read and agree to the .gov domain requirements.")

class ReviewForm(RegistrarForm):
    pass

# List of forms in our wizard. Each entry is a tuple of a name and a form
# subclass
FORMS = [
    ("organization", OrganizationForm),
    ("organization_federal", OrganizationFederalForm),
    ("organization_election", OrganizationElectionForm),
    ("org_contact", OrgContactForm),
    ("authorizing_official", AuthorizingOfficialForm),
    ("current_sites", CurrentSitesForm),
    ("dotgov_domain", DotGovDomainForm),
    ("purpose", PurposeForm),
    ("your_contact", YourContactForm),
    ("other_contacts", OtherContactsForm),
    ("security_email", SecurityEmailForm),
    ("anything_else", AnythingElseForm),
    ("requirements", RequirementsForm),
    ("review", ReviewForm),
]

# Dict to match up the right template with the right step. Keys here must
# match the first elements of the tuples in FORMS
TEMPLATES = {
    "organization": "application_organization.html",
    "organization_federal": "application_org_federal.html",
    "organization_election": "application_org_election.html",
    "org_contact": "application_org_contact.html",
    "authorizing_official": "application_authorizing_official.html",
    "current_sites": "application_current_sites.html",
    "dotgov_domain": "application_dotgov_domain.html",
    "purpose": "application_purpose.html",
    "your_contact": "application_your_contact.html",
    "other_contacts": "application_other_contacts.html",
    "security_email": "application_security_email.html",
    "anything_else": "application_anything_else.html",
    "requirements": "application_requirements.html",
    "review": "application_review.html",
}

# We need to pass our page titles as context to the templates, indexed
# by the step names
TITLES = {
    "organization": "Type of organization",
    "organization_federal": "Type of organization — Federal",
    "organization_election": "Type of organization — Election board",
    "org_contact": "Organization name and mailing address",
    "authorizing_official": "Authorizing official",
    "current_sites": "Organization website",
    "dotgov_domain": ".gov domain",
    "purpose": "Purpose of your domain",
    "your_contact": "Your contact information",
    "other_contacts": "Other contacts for your domain",
    "security_email": "Security email for public use",
    "anything_else": "Anything else we should know?",
    "requirements": "Requirements for registration and operation of .gov domains",
    "review": "Review and submit your domain request",
}


class ApplicationWizard(LoginRequiredMixin, NamedUrlSessionWizardView):

    """Multi-page form ("wizard") for new domain applications.

    This sets up a sequence of forms that gather information for new
    domain applications. Each form in the sequence has its own URL and
    the progress through the form is stored in the Django session (thus
    "NamedUrlSessionWizardView").
    """

    form_list = FORMS

    def get_template_names(self):
        """Template for the current step.

        The return is a singleton list.
        """
        return [TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        """Add title information to the context for all steps."""
        context = super().get_context_data(form=form, **kwargs)
        context["form_titles"] = TITLES
        return context

    def done(self, form_list, **kwargs):
        logger.info("Application form submitted.")
