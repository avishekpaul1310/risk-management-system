from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from risks.models import Project, Risk, Category, RiskResponse
from decimal import Decimal
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Populate the database with sample test data for testing features'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Risk.objects.all().delete()
            Project.objects.all().delete()
            Category.objects.all().delete()
            RiskResponse.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        # Create test user if it doesn't exist
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(f'Created test user: testuser / testpass123')

        # Create categories
        categories_data = [
            'Technical Risk',
            'Financial Risk', 
            'Operational Risk',
            'Security Risk',
            'Compliance Risk',
            'Market Risk',
            'Human Resources Risk',
            'Strategic Risk'
        ]
        
        categories = []
        for cat_name in categories_data:
            category, created = Category.objects.get_or_create(name=cat_name)
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {cat_name}')

        # Create projects
        projects_data = [
            {
                'name': 'E-commerce Platform Upgrade',
                'description': 'Major upgrade to the online shopping platform including new payment systems and mobile app integration.'
            },
            {
                'name': 'Data Center Migration',
                'description': 'Migration of all servers and infrastructure to a new cloud-based data center.'
            },
            {
                'name': 'Customer Portal Development',
                'description': 'Development of a new customer self-service portal with account management features.'
            },
            {
                'name': 'Security Compliance Initiative',
                'description': 'Implementation of new security measures to meet regulatory compliance requirements.'
            }
        ]

        projects = []
        for proj_data in projects_data:
            project, created = Project.objects.get_or_create(
                name=proj_data['name'],
                defaults={'description': proj_data['description']}
            )
            projects.append(project)
            if created:
                self.stdout.write(f'Created project: {proj_data["name"]}')

        # Create risks with varied likelihood/impact combinations
        risks_data = [
            # High Impact, High Likelihood (Critical Risks)
            {
                'title': 'Database Server Failure',
                'description': 'Primary database server could fail during migration causing extended downtime.',
                'likelihood': 3, 'impact': 3, 'status': 'Open',
                'category': 'Technical Risk',
                'likelihood_percentage': 75,
                'optimistic_cost_impact': Decimal('50000'),
                'most_likely_cost_impact': Decimal('150000'),
                'pessimistic_cost_impact': Decimal('500000')
            },
            {
                'title': 'Payment System Integration Failure',
                'description': 'New payment gateway integration may fail, blocking all transactions.',
                'likelihood': 3, 'impact': 3, 'status': 'Open',
                'category': 'Technical Risk',
                'likelihood_percentage': 60,
                'optimistic_cost_impact': Decimal('100000'),
                'most_likely_cost_impact': Decimal('300000'),
                'pessimistic_cost_impact': Decimal('750000')
            },
            
            # High Impact, Medium Likelihood
            {
                'title': 'Data Breach During Migration',
                'description': 'Sensitive customer data could be exposed during the migration process.',
                'likelihood': 2, 'impact': 3, 'status': 'Open',
                'category': 'Security Risk',
                'likelihood_percentage': 35,
                'optimistic_cost_impact': Decimal('200000'),
                'most_likely_cost_impact': Decimal('1000000'),
                'pessimistic_cost_impact': Decimal('5000000')
            },
            {
                'title': 'Regulatory Non-Compliance',
                'description': 'New system may not meet updated compliance requirements.',
                'likelihood': 2, 'impact': 3, 'status': 'Mitigated',
                'category': 'Compliance Risk',
                'likelihood_percentage': 40,
                'optimistic_cost_impact': Decimal('50000'),
                'most_likely_cost_impact': Decimal('250000'),
                'pessimistic_cost_impact': Decimal('1000000')
            },
            
            # High Impact, Low Likelihood
            {
                'title': 'Natural Disaster Affecting Data Center',
                'description': 'Natural disaster could destroy the new data center facility.',
                'likelihood': 1, 'impact': 3, 'status': 'Open',
                'category': 'Operational Risk',
                'likelihood_percentage': 5,
                'optimistic_cost_impact': Decimal('500000'),
                'most_likely_cost_impact': Decimal('2000000'),
                'pessimistic_cost_impact': Decimal('10000000')
            },
            
            # Medium Impact, High Likelihood
            {
                'title': 'User Adoption Resistance',
                'description': 'Users may resist adopting the new customer portal interface.',
                'likelihood': 3, 'impact': 2, 'status': 'Open',
                'category': 'Human Resources Risk',
                'likelihood_percentage': 70,
                'optimistic_cost_impact': Decimal('25000'),
                'most_likely_cost_impact': Decimal('75000'),
                'pessimistic_cost_impact': Decimal('200000')
            },
            {
                'title': 'Third-Party Vendor Delays',
                'description': 'Key vendors may deliver components late affecting project timeline.',
                'likelihood': 3, 'impact': 2, 'status': 'Open',
                'category': 'Operational Risk',
                'likelihood_percentage': 80,
                'optimistic_cost_impact': Decimal('30000'),
                'most_likely_cost_impact': Decimal('100000'),
                'pessimistic_cost_impact': Decimal('300000')
            },
            
            # Medium Impact, Medium Likelihood
            {
                'title': 'Performance Degradation',
                'description': 'New system may perform slower than expected under high load.',
                'likelihood': 2, 'impact': 2, 'status': 'Open',
                'category': 'Technical Risk',
                'likelihood_percentage': 45,
                'optimistic_cost_impact': Decimal('20000'),
                'most_likely_cost_impact': Decimal('60000'),
                'pessimistic_cost_impact': Decimal('150000')
            },
            {
                'title': 'Budget Overrun',
                'description': 'Project costs may exceed allocated budget due to scope creep.',
                'likelihood': 2, 'impact': 2, 'status': 'Mitigated',
                'category': 'Financial Risk',
                'likelihood_percentage': 50,
                'optimistic_cost_impact': Decimal('50000'),
                'most_likely_cost_impact': Decimal('125000'),
                'pessimistic_cost_impact': Decimal('400000')
            },
            
            # Medium Impact, Low Likelihood
            {
                'title': 'Key Personnel Departure',
                'description': 'Critical team members might leave during project execution.',
                'likelihood': 1, 'impact': 2, 'status': 'Open',
                'category': 'Human Resources Risk',
                'likelihood_percentage': 20,
                'optimistic_cost_impact': Decimal('15000'),
                'most_likely_cost_impact': Decimal('50000'),
                'pessimistic_cost_impact': Decimal('120000')
            },
            
            # Low Impact, High Likelihood
            {
                'title': 'Minor Interface Issues',
                'description': 'Small UI/UX issues may require post-launch fixes.',
                'likelihood': 3, 'impact': 1, 'status': 'Closed',
                'category': 'Technical Risk',
                'likelihood_percentage': 85,
                'optimistic_cost_impact': Decimal('5000'),
                'most_likely_cost_impact': Decimal('15000'),
                'pessimistic_cost_impact': Decimal('30000')
            },
            {
                'title': 'Documentation Updates Required',
                'description': 'User manuals and documentation may need frequent updates.',
                'likelihood': 3, 'impact': 1, 'status': 'Open',
                'category': 'Operational Risk',
                'likelihood_percentage': 90,
                'optimistic_cost_impact': Decimal('3000'),
                'most_likely_cost_impact': Decimal('8000'),
                'pessimistic_cost_impact': Decimal('20000')
            },
            
            # Low Impact, Medium Likelihood
            {
                'title': 'Training Session Delays',
                'description': 'Staff training sessions may be delayed due to scheduling conflicts.',
                'likelihood': 2, 'impact': 1, 'status': 'Open',
                'category': 'Human Resources Risk',
                'likelihood_percentage': 40,
                'optimistic_cost_impact': Decimal('2000'),
                'most_likely_cost_impact': Decimal('7000'),
                'pessimistic_cost_impact': Decimal('15000')
            },
            
            # Low Impact, Low Likelihood
            {
                'title': 'Minor Security Patches Needed',
                'description': 'Occasional security patches may be required for third-party components.',
                'likelihood': 1, 'impact': 1, 'status': 'Open',
                'category': 'Security Risk',
                'likelihood_percentage': 25,
                'optimistic_cost_impact': Decimal('1000'),
                'most_likely_cost_impact': Decimal('3000'),
                'pessimistic_cost_impact': Decimal('8000')
            }
        ]

        # Create risks
        created_risks = []
        for i, risk_data in enumerate(risks_data):
            # Assign to projects in round-robin fashion
            project = projects[i % len(projects)]
            category = next((cat for cat in categories if cat.name == risk_data['category']), categories[0])
            
            risk, created = Risk.objects.get_or_create(
                title=risk_data['title'],
                project=project,
                defaults={
                    'description': risk_data['description'],
                    'likelihood': risk_data['likelihood'],
                    'impact': risk_data['impact'],
                    'status': risk_data['status'],
                    'category': category,
                    'owner': f'Team Lead {i % 3 + 1}',
                    'likelihood_percentage': risk_data['likelihood_percentage'],
                    'optimistic_cost_impact': risk_data['optimistic_cost_impact'],
                    'most_likely_cost_impact': risk_data['most_likely_cost_impact'],
                    'pessimistic_cost_impact': risk_data['pessimistic_cost_impact']
                }
            )
            if created:
                created_risks.append(risk)
                self.stdout.write(f'Created risk: {risk_data["title"]} (Impact: {risk_data["impact"]}, Likelihood: {risk_data["likelihood"]})')

        # Create some sample risk responses
        response_data = [
            {
                'type': 'Mitigate',
                'description': 'Implement automated backup systems and failover procedures.',
                'cost_estimate': Decimal('25000'),
                'currency': 'USD'
            },
            {
                'type': 'Transfer',
                'description': 'Purchase comprehensive cyber insurance coverage.',
                'cost_estimate': Decimal('15000'),
                'currency': 'USD'
            },
            {
                'type': 'Accept',
                'description': 'Accept the risk and establish contingency funds.',
                'cost_estimate': Decimal('0'),
                'currency': 'USD'
            }
        ]

        # Add responses to some risks
        for i, response in enumerate(response_data):
            if i < len(created_risks):
                risk_response, created = RiskResponse.objects.get_or_create(
                    risk=created_risks[i],
                    type=response['type'],
                    defaults={
                        'description': response['description'],
                        'cost_estimate': response['cost_estimate'],
                        'currency': response['currency'],
                        'created_by': user
                    }
                )
                if created:
                    self.stdout.write(f'Created risk response for: {created_risks[i].title}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully populated database with:\n'
                f'- {len(categories)} categories\n'
                f'- {len(projects)} projects\n'
                f'- {len(created_risks)} risks\n'
                f'- Various risk responses\n\n'
                f'You can now test the dashboard and other features!\n'
                f'Login credentials: testuser / testpass123'
            )
        )
