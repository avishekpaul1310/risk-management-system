import unittest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from risks.models import Project, Risk, Category
from risks.forms import ProjectForm, RiskForm, CategoryForm


class ModelTests(TestCase):
    """Tests for the data models"""
    
    def setUp(self):
        # Create a test project
        self.project = Project.objects.create(
            name="Test Project",
            description="A project created for testing"
        )
        
        # Create a test category
        self.category = Category.objects.create(
            name="Test Category",
            description="A category created for testing"
        )
        
        # Create a test risk
        self.risk = Risk.objects.create(
            project=self.project,
            title="Test Risk",
            description="A risk created for testing",
            category=self.category,
            likelihood=2,  # Medium
            impact=3,      # High
            owner="Test Owner",
            status="Open"
        )
    
    def test_project_creation(self):
        """Test the creation of a project and its string representation"""
        self.assertEqual(self.project.name, "Test Project")
        self.assertEqual(str(self.project), "Test Project")
    
    def test_category_creation(self):
        """Test the creation of a category and its string representation"""
        self.assertEqual(self.category.name, "Test Category")
        self.assertEqual(str(self.category), "Test Category")
    
    def test_risk_creation(self):
        """Test the creation of a risk"""
        self.assertEqual(self.risk.title, "Test Risk")
        self.assertEqual(self.risk.project, self.project)
        self.assertEqual(self.risk.category, self.category)
        self.assertEqual(self.risk.likelihood, 2)
        self.assertEqual(self.risk.impact, 3)
        self.assertEqual(self.risk.owner, "Test Owner")
        self.assertEqual(self.risk.status, "Open")
    
    def test_risk_score_calculation(self):
        """Test that risk_score is calculated correctly"""
        # risk_score = likelihood * impact
        self.assertEqual(self.risk.risk_score, 6)  # 2 * 3 = 6
    
    def test_risk_level_property(self):
        """Test that risk_level is determined correctly based on risk_score"""
        # High risk: score >= 6
        self.risk.likelihood = 3
        self.risk.impact = 3
        self.assertEqual(self.risk.risk_score, 9)
        self.assertEqual(self.risk.risk_level, "High")
        
        # Medium risk: 3 <= score < 6
        self.risk.likelihood = 1
        self.risk.impact = 3
        self.assertEqual(self.risk.risk_score, 3)
        self.assertEqual(self.risk.risk_level, "Medium")
        
        # Low risk: score < 3
        self.risk.likelihood = 1
        self.risk.impact = 1
        self.assertEqual(self.risk.risk_score, 1)
        self.assertEqual(self.risk.risk_level, "Low")
    
    def test_risk_string_representation(self):
        """Test the string representation of a risk"""
        expected_str = f"Test Risk (Test Project)"
        self.assertEqual(str(self.risk), expected_str)


class FormTests(TestCase):
    """Tests for the forms"""
    
    def setUp(self):
        # Create a test category
        self.category = Category.objects.create(
            name="Test Category",
            description="A category created for testing"
        )
        
        # Create a test project
        self.project = Project.objects.create(
            name="Test Project",
            description="A project created for testing"
        )
    
    def test_project_form_valid_data(self):
        """Test project form with valid data"""
        form_data = {
            'name': 'New Project',
            'description': 'Description for the new project'
        }
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_project_form_invalid_data(self):
        """Test project form with invalid data (no name)"""
        form_data = {
            'name': '',  # Name is required
            'description': 'Description for the new project'
        }
        form = ProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
    
    def test_category_form_valid_data(self):
        """Test category form with valid data"""
        form_data = {
            'name': 'New Category',
            'description': 'Description for the new category'
        }
        form = CategoryForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_category_form_invalid_data(self):
        """Test category form with invalid data (duplicate name)"""
        # Create a form with the same name as an existing category
        form_data = {
            'name': 'Test Category',  # This name already exists
            'description': 'Another description'
        }
        form = CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
    
    def test_risk_form_valid_data(self):
        """Test risk form with valid data"""
        form_data = {
            'title': 'New Risk',
            'description': 'Description for the new risk',
            'category': self.category.id,
            'likelihood': 2,
            'impact': 2,
            'owner': 'Risk Owner',
            'status': 'Open'
        }
        form = RiskForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_risk_form_invalid_data(self):
        """Test risk form with invalid data (invalid likelihood)"""
        form_data = {
            'title': 'New Risk',
            'description': 'Description for the new risk',
            'category': self.category.id,
            'likelihood': 5,  # Invalid choice (should be 1, 2, or 3)
            'impact': 2,
            'owner': 'Risk Owner',
            'status': 'Open'
        }
        form = RiskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('likelihood', form.errors)


class ViewTests(TestCase):
    """Tests for the views"""
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Create a test client
        self.client = Client()
        
        # Create a test category
        self.category = Category.objects.create(
            name="Test Category",
            description="A category created for testing"
        )
        
        # Create a test project
        self.project = Project.objects.create(
            name="Test Project",
            description="A project created for testing"
        )
        
        # Create a test risk
        self.risk = Risk.objects.create(
            project=self.project,
            title="Test Risk",
            description="A risk created for testing",
            category=self.category,
            likelihood=2,
            impact=3,
            owner="Test Owner",
            status="Open"
        )
    
    def test_home_view_not_authenticated(self):
        """Test home view redirects to login if user is not authenticated"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn('/accounts/login/', response.url)
    
    def test_home_view_authenticated(self):
        """Test home view works if user is authenticated"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'risks/home.html')
        self.assertContains(response, 'Test Project')
    
    def test_project_detail_view(self):
        """Test project detail view"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('project_detail', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'risks/project_detail.html')
        self.assertContains(response, 'Test Project')
        self.assertContains(response, 'Test Risk')
    
    def test_add_project_view(self):
        """Test add project view"""
        self.client.login(username='testuser', password='testpassword')
        
        # GET request
        response = self.client.get(reverse('add_project'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'risks/add_project.html')
        
        # POST request with valid data
        project_data = {
            'name': 'New Project',
            'description': 'Description for the new project'
        }
        response = self.client.post(reverse('add_project'), project_data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        
        # Check that the project was created
        self.assertTrue(Project.objects.filter(name='New Project').exists())
    
    def test_edit_project_view(self):
        """Test edit project view"""
        self.client.login(username='testuser', password='testpassword')
        
        # GET request
        response = self.client.get(reverse('edit_project', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'risks/edit_project.html')
        
        # POST request with valid data
        project_data = {
            'name': 'Updated Project Name',
            'description': 'Updated description'
        }
        response = self.client.post(reverse('edit_project', args=[self.project.id]), project_data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        
        # Check that the project was updated
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, 'Updated Project Name')
        self.assertEqual(self.project.description, 'Updated description')
    
    def test_add_risk_view(self):
        """Test add risk view"""
        self.client.login(username='testuser', password='testpassword')
        
        # GET request
        response = self.client.get(reverse('add_risk', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'risks/add_risk.html')
        
        # POST request with valid data
        risk_data = {
            'title': 'New Risk',
            'description': 'Description for the new risk',
            'category': self.category.id,
            'likelihood': 2,
            'impact': 2,
            'owner': 'Risk Owner',
            'status': 'Open'
        }
        response = self.client.post(reverse('add_risk', args=[self.project.id]), risk_data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        
        # Check that the risk was created
        self.assertTrue(Risk.objects.filter(title='New Risk').exists())
    
    def test_edit_risk_view(self):
        """Test edit risk view"""
        self.client.login(username='testuser', password='testpassword')
        
        # GET request
        response = self.client.get(reverse('edit_risk', args=[self.risk.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'risks/edit_risk.html')
        
        # POST request with valid data
        risk_data = {
            'title': 'Updated Risk Title',
            'description': 'Updated risk description',
            'category': self.category.id,
            'likelihood': 3,
            'impact': 3,
            'owner': 'Updated Owner',
            'status': 'Mitigated'
        }
        response = self.client.post(reverse('edit_risk', args=[self.risk.id]), risk_data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        
        # Check that the risk was updated
        self.risk.refresh_from_db()
        self.assertEqual(self.risk.title, 'Updated Risk Title')
        self.assertEqual(self.risk.likelihood, 3)
        self.assertEqual(self.risk.impact, 3)
        self.assertEqual(self.risk.status, 'Mitigated')
    
    def test_delete_risk_view(self):
        """Test delete risk view"""
        self.client.login(username='testuser', password='testpassword')
        
        # GET request (confirmation page)
        response = self.client.get(reverse('delete_risk', args=[self.risk.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'risks/delete_risk.html')
        
        # POST request (actual deletion)
        response = self.client.post(reverse('delete_risk', args=[self.risk.id]))
        self.assertEqual(response.status_code, 302)  # Redirect on success
        
        # Check that the risk was deleted
        self.assertFalse(Risk.objects.filter(id=self.risk.id).exists())
    
    def test_categories_view(self):
        """Test categories view"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'risks/categories.html')
        self.assertContains(response, 'Test Category')
    
    def test_dashboard_view(self):
        """Test dashboard view"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'risks/dashboard.html')
        self.assertContains(response, 'Risk Management Dashboard')
    
    def test_export_risks_csv(self):
        """Test CSV export functionality"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('export_risks_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertTrue('attachment; filename="risks_export_' in response['Content-Disposition'])


class AuthenticationTests(TestCase):
    """Tests for user authentication"""
    
    def setUp(self):
        # Create a test client
        self.client = Client()
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
    def test_login_view(self):
        """Test the login view"""
        # GET request
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'risks/login.html')
        
        # POST request with valid credentials
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertRedirects(response, reverse('home'))
        
        # Check if user is logged in
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_view_invalid_credentials(self):
        """Test login view with invalid credentials"""
        login_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 200)  # Returns to login page
        self.assertContains(response, "Your username and password didn't match")
    
    def test_logout_view(self):
        """Test the logout view"""
        # Login first
        self.client.login(username='testuser', password='testpassword')
        
        # Verify login successful
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Logout
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        
        # Check if user is logged out
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_signup_view(self):
        """Test the signup view"""
        # GET request
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'risks/signup.html')
        
        # POST request with valid data
        signup_data = {
            'username': 'newuser',
            'password1': 'complex_password123',
            'password2': 'complex_password123'
        }
        response = self.client.post(reverse('signup'), signup_data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        
        # Check if user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_profile_view(self):
        """Test the profile view"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'risks/profile.html')
        self.assertContains(response, 'testuser')


class CategoryFunctionalityTests(TestCase):
    """Tests specifically for category functionality"""
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Create a test client
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        
        # Create test categories
        self.category1 = Category.objects.create(
            name="Test Category 1",
            description="First test category"
        )
        
        self.category2 = Category.objects.create(
            name="Test Category 2",
            description="Second test category"
        )
        
        # Create a test project
        self.project = Project.objects.create(
            name="Test Project",
            description="A project created for testing"
        )
    
    def test_add_category_view(self):
        """Test add category view"""
        # GET request
        response = self.client.get(reverse('add_category'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'risks/add_category.html')
        
        # POST request with valid data
        category_data = {
            'name': 'New Category',
            'description': 'Description for the new category'
        }
        response = self.client.post(reverse('add_category'), category_data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        
        # Check that the category was created
        self.assertTrue(Category.objects.filter(name='New Category').exists())
    
    def test_edit_category_view(self):
        """Test edit category view"""
        # GET request
        response = self.client.get(reverse('edit_category', args=[self.category1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'risks/edit_category.html')
        
        # POST request with valid data
        category_data = {
            'name': 'Updated Category Name',
            'description': 'Updated description'
        }
        response = self.client.post(reverse('edit_category', args=[self.category1.id]), category_data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        
        # Check that the category was updated
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.name, 'Updated Category Name')
        self.assertEqual(self.category1.description, 'Updated description')
    
    def test_delete_category_view(self):
        """Test delete category view"""
        # GET request (confirmation page)
        response = self.client.get(reverse('delete_category', args=[self.category2.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'risks/delete_category.html')
        
        # POST request (actual deletion)
        response = self.client.post(reverse('delete_category', args=[self.category2.id]))
        self.assertEqual(response.status_code, 302)  # Redirect on success
        
        # Check that the category was deleted
        self.assertFalse(Category.objects.filter(id=self.category2.id).exists())
    
    def test_cant_delete_category_in_use(self):
        """Test that a category can't be deleted if it's used by risks"""
        # Create a risk using category1
        risk = Risk.objects.create(
            project=self.project,
            title="Test Risk",
            description="A risk created for testing",
            category=self.category1,
            likelihood=2,
            impact=3,
            owner="Test Owner",
            status="Open"
        )
        
        # Try to delete the category
        response = self.client.post(reverse('delete_category', args=[self.category1.id]))
        
        # Check that the category wasn't deleted
        self.assertTrue(Category.objects.filter(id=self.category1.id).exists())
        
        # Check for error message
        response = self.client.get(reverse('categories'))
        messages = list(response.context['messages'])
        self.assertTrue(any("Cannot delete category" in str(message) for message in messages))


class RiskCalculationTests(TestCase):
    """Tests for risk calculation functionality"""
    
    def setUp(self):
        # Create a test project
        self.project = Project.objects.create(
            name="Test Project",
            description="A project created for testing"
        )
        
        # Create a test category
        self.category = Category.objects.create(
            name="Test Category",
            description="A category created for testing"
        )
        
        # Create risks with different severity levels
        # High risk (likelihood=3, impact=3)
        self.high_risk = Risk.objects.create(
            project=self.project,
            title="High Risk",
            description="A high risk for testing",
            category=self.category,
            likelihood=3,
            impact=3,
            owner="Test Owner",
            status="Open"
        )
        
        # Medium risk (likelihood=2, impact=2)
        self.medium_risk = Risk.objects.create(
            project=self.project,
            title="Medium Risk",
            description="A medium risk for testing",
            category=self.category,
            likelihood=2,
            impact=2,
            owner="Test Owner",
            status="Open"
        )
        
        # Low risk (likelihood=1, impact=1)
        self.low_risk = Risk.objects.create(
            project=self.project,
            title="Low Risk",
            description="A low risk for testing",
            category=self.category,
            likelihood=1,
            impact=1,
            owner="Test Owner",
            status="Open"
        )
    
    def test_risk_score_calculation(self):
        """Test that risk scores are calculated correctly"""
        self.assertEqual(self.high_risk.risk_score, 9)    # 3 * 3 = 9
        self.assertEqual(self.medium_risk.risk_score, 4)  # 2 * 2 = 4
        self.assertEqual(self.low_risk.risk_score, 1)     # 1 * 1 = 1
    
    def test_risk_level_classification(self):
        """Test that risks are classified correctly based on their scores"""
        self.assertEqual(self.high_risk.risk_level, "High")
        self.assertEqual(self.medium_risk.risk_level, "Medium")
        self.assertEqual(self.low_risk.risk_level, "Low")
    
    def test_risk_ordering_in_project_detail(self):
        """Test that risks are ordered correctly (by severity) in project detail view"""
        # Log in first
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        
        # Get project detail view
        response = self.client.get(reverse('project_detail', args=[self.project.id]))
        
        # Get the ordered list of risks from the context
        risks = response.context['risks']
        
        # Check the order (should be high, medium, low)
        self.assertEqual(risks[0], self.high_risk)
        self.assertEqual(risks[1], self.medium_risk)
        self.assertEqual(risks[2], self.low_risk)
    
    def test_dashboard_risk_statistics(self):
        """Test that the dashboard correctly calculates risk statistics"""
        # Log in first
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        
        # Get dashboard view
        response = self.client.get(reverse('dashboard'))
        
        # Check risk counts
        self.assertEqual(response.context['risk_count'], 3)
        self.assertEqual(response.context['high_risks'], 1)
        self.assertEqual(response.context['medium_risks'], 1)
        self.assertEqual(response.context['low_risks'], 1)
        
        # Check open risks count
        self.assertEqual(response.context['open_risks'], 3)
        
        # Check severity data for chart
        severity_data = response.context['severity_data']
        self.assertEqual(severity_data['high'], 1)
        self.assertEqual(severity_data['medium'], 1)
        self.assertEqual(severity_data['low'], 1)


class CSVExportTests(TestCase):
    """Tests for CSV export functionality"""
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Create a test client
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        
        # Create a test project
        self.project = Project.objects.create(
            name="Test Project",
            description="A project created for testing"
        )
        
        # Create a test category
        self.category = Category.objects.create(
            name="Test Category",
            description="A category created for testing"
        )
        
        # Create a test risk
        self.risk = Risk.objects.create(
            project=self.project,
            title="Test Risk",
            description="A risk created for testing",
            category=self.category,
            likelihood=2,
            impact=3,
            owner="Test Owner",
            status="Open"
        )
    
    def test_csv_export_content(self):
        """Test that the CSV export contains the correct content"""
        response = self.client.get(reverse('export_risks_csv'))
        
        # Check the response type
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        
        # Convert the response content to string
        content = response.content.decode('utf-8')
        
        # Check that the headers are present
        self.assertIn('Project,Risk Title,Description,Category,Likelihood,Impact,Risk Score,Risk Level,Owner,Status', content)
        
        # Check that the risk data is present
        self.assertIn('Test Project,Test Risk,A risk created for testing,Test Category,Medium,High,6,High,Test Owner,Open', content)


class PermissionAndSecurityTests(TestCase):
    """Tests for permissions and security features"""
    
    def setUp(self):
        # Create two test users
        self.user1 = User.objects.create_user(
            username='user1',
            password='password1'
        )
        
        self.user2 = User.objects.create_user(
            username='user2',
            password='password2'
        )
        
        # Create an admin user
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpassword',
            email='admin@example.com'
        )
        
        # Create a test client
        self.client = Client()
        
        # Create a test project
        self.project = Project.objects.create(
            name="Test Project",
            description="A project created for testing"
        )
        
        # Create a test category
        self.category = Category.objects.create(
            name="Test Category",
            description="A category created for testing"
        )
        
        # Create a test risk
        self.risk = Risk.objects.create(
            project=self.project,
            title="Test Risk",
            description="A risk created for testing",
            category=self.category,
            likelihood=2,
            impact=3,
            owner="Test Owner",
            status="Open"
        )
    
    def test_login_required(self):
        """Test that login is required for protected views"""
        # List of URLs that should require login
        protected_urls = [
            reverse('home'),
            reverse('project_detail', args=[self.project.id]),
            reverse('add_project'),
            reverse('edit_project', args=[self.project.id]),
            reverse('categories'),
            reverse('add_category'),
            reverse('edit_category', args=[self.category.id]),
            reverse('delete_category', args=[self.category.id]),
            reverse('add_risk', args=[self.project.id]),
            reverse('edit_risk', args=[self.risk.id]),
            reverse('delete_risk', args=[self.risk.id]),
            reverse('dashboard'),
            reverse('profile'),
            reverse('export_risks_csv'),
        ]
        
        # Check each URL without being logged in
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)  # Should redirect to login
            self.assertIn('/accounts/login/', response.url)
    
    def test_admin_access(self):
        """Test that admin users can access the admin interface"""
        # Try to access the admin site
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)  # Should redirect to admin login
        
        # Login as admin
        self.client.login(username='admin', password='adminpassword')
        
        # Try again
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)  # Should be accessible
    
    def test_non_admin_cannot_access_admin(self):
        """Test that non-admin users cannot access the admin interface"""
        # Login as a non-admin user
        self.client.login(username='user1', password='password1')
        
        # Try to access the admin site
        response = self.client.get('/admin/')
        self.assertNotEqual(response.status_code, 200)  # Should not be accessible
    
    def test_csrf_protection(self):
        """Test that CSRF protection is enforced for POST requests"""
        # Login
        self.client.login(username='user1', password='password1')
        
        # Try to submit a form without CSRF token
        self.client.handler.enforce_csrf_checks = True
        
        # Attempt to add a project without CSRF token
        project_data = {
            'name': 'CSRF Test Project',
            'description': 'This should not be added'
        }
        response = self.client.post(reverse('add_project'), project_data)
        
        # Should be forbidden
        self.assertEqual(response.status_code, 403)  # Forbidden due to CSRF
        
        # Verify the project was not added
        self.assertFalse(Project.objects.filter(name='CSRF Test Project').exists())


class EdgeCaseTests(TestCase):
    """Tests for edge cases and corner scenarios"""
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Create a test client
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        
        # Create a test project
        self.project = Project.objects.create(
            name="Test Project",
            description="A project created for testing"
        )
        
        # Create a test category
        self.category = Category.objects.create(
            name="Test Category",
            description="A category created for testing"
        )
    
    def test_very_long_inputs(self):
        """Test handling of very long inputs"""
        # Create a risk with very long title and description
        long_title = "A" * 100  # Max length is 100
        long_description = "B" * 1000
        
        risk_data = {
            'title': long_title,
            'description': long_description,
            'category': self.category.id,
            'likelihood': 2,
            'impact': 2,
            'owner': 'Risk Owner',
            'status': 'Open'
        }
        
        response = self.client.post(reverse('add_risk', args=[self.project.id]), risk_data)
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        
        # Check that the risk was created with full title and description
        created_risk = Risk.objects.get(title=long_title)
        self.assertEqual(created_risk.title, long_title)
        self.assertEqual(created_risk.description, long_description)
    
    def test_project_with_no_risks(self):
        """Test project detail view for a project with no risks"""
        # Create a new project with no risks
        empty_project = Project.objects.create(
            name="Empty Project",
            description="A project with no risks"
        )
        
        # View the project
        response = self.client.get(reverse('project_detail', args=[empty_project.id]))
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No risks added to this project yet")
        
        # Check that the risk stats are all zeros
        risk_stats = response.context['risk_stats']
        self.assertEqual(risk_stats['total'], 0)
        self.assertEqual(risk_stats['high'], 0)
        self.assertEqual(risk_stats['medium'], 0)
        self.assertEqual(risk_stats['low'], 0)
        self.assertEqual(risk_stats['open'], 0)
        self.assertEqual(risk_stats['mitigated'], 0)
        self.assertEqual(risk_stats['closed'], 0)
    
    def test_deleting_project_deletes_risks(self):
        """Test that deleting a project also deletes all associated risks"""
        # Create a risk for the project
        risk = Risk.objects.create(
            project=self.project,
            title="Test Risk",
            description="A risk created for testing",
            category=self.category,
            likelihood=2,
            impact=3,
            owner="Test Owner",
            status="Open"
        )
        
        # Delete the project
        self.project.delete()
        
        # Check that the risk is also deleted
        self.assertFalse(Risk.objects.filter(id=risk.id).exists())
    
    def test_risk_with_no_category(self):
        """Test that a risk can be created without a category (null=True)"""
        # Create a risk without a category
        risk = Risk.objects.create(
            project=self.project,
            title="No Category Risk",
            description="A risk with no category",
            category=None,  # This should be allowed because category can be null
            likelihood=2,
            impact=3,
            owner="Test Owner",
            status="Open"
        )
        
        # Check that the risk was created
        self.assertEqual(risk.title, "No Category Risk")
        self.assertIsNone(risk.category)
    
    def test_special_characters_in_inputs(self):
        """Test handling of special characters in inputs"""
        # Create a project with special characters
        special_name = "Project with special chars: !@#$%^&*()_+-={}[]|\\:;\"'<>,.?/~`"
        special_desc = "Description with special chars: !@#$%^&*()_+-={}[]|\\:;\"'<>,.?/~`"
        
        project_data = {
            'name': special_name,
            'description': special_desc
        }
        
        response = self.client.post(reverse('add_project'), project_data)
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        
        # Check that the project was created with correct special characters
        created_project = Project.objects.get(name=special_name)
        self.assertEqual(created_project.name, special_name)
        self.assertEqual(created_project.description, special_desc)


class ModelValidationTests(TestCase):
    """Tests for model validation"""
    
    def setUp(self):
        # Create a test project
        self.project = Project.objects.create(
            name="Test Project",
            description="A project created for testing"
        )
        
        # Create a test category
        self.category = Category.objects.create(
            name="Test Category",
            description="A category created for testing"
        )
    
    def test_risk_model_constraints(self):
        """Test constraints on the Risk model"""
        # Test that title is required
        with self.assertRaises(ValidationError):
            Risk.objects.create(
                project=self.project,
                title="",  # Empty title should raise error
                description="A risk created for testing",
                category=self.category,
                likelihood=2,
                impact=3,
                owner="Test Owner",
                status="Open"
            )
        
        # Test that likelihood must be a valid choice
        with self.assertRaises(ValidationError):
            Risk.objects.create(
                project=self.project,
                title="Test Risk",
                description="A risk created for testing",
                category=self.category,
                likelihood=5,  # Invalid choice
                impact=3,
                owner="Test Owner",
                status="Open"
            )
        
        # Test that impact must be a valid choice
        with self.assertRaises(ValidationError):
            Risk.objects.create(
                project=self.project,
                title="Test Risk",
                description="A risk created for testing",
                category=self.category,
                likelihood=2,
                impact=5,  # Invalid choice
                owner="Test Owner",
                status="Open"
            )
        
        # Test that status must be a valid choice
        with self.assertRaises(ValidationError):
            Risk.objects.create(
                project=self.project,
                title="Test Risk",
                description="A risk created for testing",
                category=self.category,
                likelihood=2,
                impact=3,
                owner="Test Owner",
                status="InvalidStatus"  # Invalid choice
            )
    
    def test_category_uniqueness(self):
        """Test that category names must be unique"""
        # Try to create a category with the same name
        with self.assertRaises(Exception):  # Could be IntegrityError or ValidationError
            Category.objects.create(
                name="Test Category",  # Already exists
                description="Another category with the same name"
            )


class IntegrationTests(TestCase):
    """Integration tests that test multiple parts of the system together"""
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Create a test client
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
    
    def test_complete_risk_workflow(self):
        """Test the complete risk management workflow"""
        # 1. Create a new project
        project_data = {
            'name': 'Integration Test Project',
            'description': 'Project for integration testing'
        }
        response = self.client.post(reverse('add_project'), project_data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        
        # Get the created project
        project = Project.objects.get(name='Integration Test Project')
        
        # 2. Create a new category
        category_data = {
            'name': 'Integration Test Category',
            'description': 'Category for integration testing'
        }
        response = self.client.post(reverse('add_category'), category_data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        
        # Get the created category
        category = Category.objects.get(name='Integration Test Category')
        
        # 3. Add a risk to the project
        risk_data = {
            'title': 'Integration Test Risk',
            'description': 'Risk for integration testing',
            'category': category.id,
            'likelihood': 3,
            'impact': 3,
            'owner': 'Integration Tester',
            'status': 'Open'
        }
        response = self.client.post(reverse('add_risk', args=[project.id]), risk_data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        
        # Get the created risk
        risk = Risk.objects.get(title='Integration Test Risk')
        
        # 4. View the project detail
        response = self.client.get(reverse('project_detail', args=[project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Integration Test Risk')
        self.assertContains(response, 'Integration Test Category')
        
        # 5. Update the risk
        updated_risk_data = {
            'title': 'Updated Integration Test Risk',
            'description': 'Updated risk description',
            'category': category.id,
            'likelihood': 2,
            'impact': 2,
            'owner': 'Updated Owner',
            'status': 'Mitigated'
        }
        response = self.client.post(reverse('edit_risk', args=[risk.id]), updated_risk_data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        
        # Get the updated risk
        risk.refresh_from_db()
        self.assertEqual(risk.title, 'Updated Integration Test Risk')
        self.assertEqual(risk.status, 'Mitigated')
        
        # 6. Check the dashboard
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # 7. Delete the risk
        response = self.client.post(reverse('delete_risk', args=[risk.id]))
        self.assertEqual(response.status_code, 302)  # Redirect on success
        
        # Verify the risk is deleted
        self.assertFalse(Risk.objects.filter(id=risk.id).exists())
    
    def test_dashboard_with_multiple_projects(self):
        """Test the dashboard with multiple projects and risks"""
        # Create two projects
        project1 = Project.objects.create(
            name="Integration Project 1",
            description="First integration test project"
        )
        
        project2 = Project.objects.create(
            name="Integration Project 2",
            description="Second integration test project"
        )
        
        # Create a category
        category = Category.objects.create(
            name="Integration Category",
            description="Category for integration testing"
        )
        
        # Create risks with different levels and statuses
        # High risk, Open
        Risk.objects.create(
            project=project1,
            title="High Risk 1",
            description="A high risk for testing",
            category=category,
            likelihood=3,
            impact=3,
            owner="Test Owner",
            status="Open"
        )
        
        # High risk, Mitigated
        Risk.objects.create(
            project=project1,
            title="High Risk 2",
            description="Another high risk for testing",
            category=category,
            likelihood=3,
            impact=3,
            owner="Test Owner",
            status="Mitigated"
        )
        
        # Medium risk, Open
        Risk.objects.create(
            project=project2,
            title="Medium Risk",
            description="A medium risk for testing",
            category=category,
            likelihood=2,
            impact=2,
            owner="Test Owner",
            status="Open"
        )
        
        # Low risk, Closed
        Risk.objects.create(
            project=project2,
            title="Low Risk",
            description="A low risk for testing",
            category=category,
            likelihood=1,
            impact=1,
            owner="Test Owner",
            status="Closed"
        )
        
        # Visit the dashboard
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Check project count
        self.assertEqual(response.context['project_count'], 2)
        
        # Check risk counts
        self.assertEqual(response.context['risk_count'], 4)
        self.assertEqual(response.context['high_risks'], 2)
        self.assertEqual(response.context['medium_risks'], 1)
        self.assertEqual(response.context['low_risks'], 1)
        
        # Check status counts
        self.assertEqual(response.context['open_risks'], 2)
        self.assertEqual(response.context['mitigated_risks'], 1)
        self.assertEqual(response.context['closed_risks'], 1)
        
        # Check high priority risks
        high_priority_risks = response.context['high_priority_risks']
        self.assertEqual(len(high_priority_risks), 2)
        self.assertTrue(all(risk.status == 'Open' for risk in high_priority_risks))
    
    def test_export_csv_functionality(self):
        """Test the CSV export functionality with multiple risks"""
        # Create a project
        project = Project.objects.create(
            name="CSV Export Project",
            description="Project for testing CSV export"
        )
        
        # Create a category
        category = Category.objects.create(
            name="CSV Export Category",
            description="Category for testing CSV export"
        )
        
        # Create multiple risks
        for i in range(1, 4):
            Risk.objects.create(
                project=project,
                title=f"CSV Risk {i}",
                description=f"Description for CSV Risk {i}",
                category=category,
                likelihood=i,
                impact=i,
                owner=f"Owner {i}",
                status="Open" if i < 3 else "Mitigated"
            )
        
        # Get the CSV export
        response = self.client.get(reverse('export_risks_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        
        # Convert the response content to string
        content = response.content.decode('utf-8')
        
        # Check that all risks are included
        for i in range(1, 4):
            self.assertIn(f"CSV Risk {i}", content)
            self.assertIn(f"Description for CSV Risk {i}", content)
            self.assertIn(f"Owner {i}", content)
        
        # Check that the status is correctly included
        self.assertIn("Open", content)
        self.assertIn("Mitigated", content)


if __name__ == '__main__':
    unittest.main()