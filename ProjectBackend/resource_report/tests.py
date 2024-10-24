from django.test import TestCase
from django.contrib.auth.models import User
from resource_contribution.models import RESOURCE_METADATA
from .models import RESOURCE_REPORT

#unit test - resource report MODEL
class RESOURCE_REPORTTest(TestCase):
    def setUp(self):
        # Create a user instance for testing
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create a RESOURCE_METADATA instance for testing
        self.resource_metadata = RESOURCE_METADATA.objects.create(
            # Assuming there are fields like 'name' and 'description' in RESOURCE_METADATA
            contributor= self.user,
            resource_name= "TEST RESOURCE",
            subject= "SUBJECT TEST",
            grade= "GRADE TEST",
            keywords= "test1, test2, test3",
            approval_status= "pending"
            
        )

    def test_resource_report_creation(self):
        # Create an instance of RESOURCE_REPORT
        report = RESOURCE_REPORT.objects.create(
            reportResource=self.resource_metadata,
            reportComplaint='This is a complaint.',
            reportUser=self.user
        )
        
        # Verify that the report was created successfully
        self.assertEqual(report.reportResource, self.resource_metadata)
        self.assertEqual(report.reportComplaint, 'This is a complaint.')
        self.assertEqual(report.reportUser, self.user)
        
    def test_report_datetime_auto_now_add(self):
        # Create an instance of RESOURCE_REPORT without saving it yet
        report = RESOURCE_REPORT(
            reportResource=self.resource_metadata,
            reportComplaint='Another complaint.',
            reportUser=self.user
        )
        
        # Check that the datetime field is None before saving
        self.assertIsNone(report.reportDatetime)
        
        # Save the instance to trigger auto_now_add behavior
        report.save()
        
        # Check that the datetime field is now set to current time after saving
        self.assertIsNotNone(report.reportDatetime)