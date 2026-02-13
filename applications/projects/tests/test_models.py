"""
Unit tests for LayerGroup color field validation
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from applications.projects.models import LayerGroup, Project


class LayerGroupColorTests(TestCase):
    """Test cases for LayerGroup color field"""

    def setUp(self):
        """Set up test data"""
        self.project = Project.objects.create(
            nombre_corto='test',
            nombre='Test Project',
            coordenada_central_x=-74.0,
            coordenada_central_y=4.0
        )

    def test_valid_6_digit_color(self):
        """Test valid 6-digit hex color"""
        group = LayerGroup.objects.create(
            proyecto=self.project,
            nombre='Test Group',
            color='#FF5733'
        )
        self.assertEqual(group.color, '#FF5733')

    def test_valid_3_digit_color(self):
        """Test valid 3-digit hex color"""
        group = LayerGroup.objects.create(
            proyecto=self.project,
            nombre='Test Group',
            color='#F57'
        )
        self.assertEqual(group.color, '#F57')

    def test_default_color(self):
        """Test default color value"""
        group = LayerGroup.objects.create(
            proyecto=self.project,
            nombre='Test Group'
        )
        self.assertEqual(group.color, '#e3e3e3')

    def test_lowercase_hex_color(self):
        """Test lowercase hex color is accepted"""
        group = LayerGroup.objects.create(
            proyecto=self.project,
            nombre='Test Group',
            color='#ff5733'
        )
        self.assertEqual(group.color, '#ff5733')

    def test_mixed_case_hex_color(self):
        """Test mixed case hex color is accepted"""
        group = LayerGroup.objects.create(
            proyecto=self.project,
            nombre='Test Group',
            color='#Ff5733'
        )
        self.assertEqual(group.color, '#Ff5733')

    def test_invalid_color_format(self):
        """Test invalid color format raises validation error"""
        group = LayerGroup(
            proyecto=self.project,
            nombre='Test Group',
            color='invalid'
        )
        with self.assertRaises(ValidationError) as context:
            group.full_clean()
        self.assertIn('color', context.exception.message_dict)

    def test_color_without_hash(self):
        """Test color without # prefix raises validation error"""
        group = LayerGroup(
            proyecto=self.project,
            nombre='Test Group',
            color='FF5733'
        )
        with self.assertRaises(ValidationError) as context:
            group.full_clean()
        self.assertIn('color', context.exception.message_dict)

    def test_invalid_hex_characters(self):
        """Test invalid hex characters raise validation error"""
        group = LayerGroup(
            proyecto=self.project,
            nombre='Test Group',
            color='#GG5733'
        )
        with self.assertRaises(ValidationError) as context:
            group.full_clean()
        self.assertIn('color', context.exception.message_dict)

    def test_wrong_length_color(self):
        """Test wrong length color raises validation error"""
        # 4 digits (invalid)
        group = LayerGroup(
            proyecto=self.project,
            nombre='Test Group',
            color='#FF57'
        )
        with self.assertRaises(ValidationError) as context:
            group.full_clean()
        self.assertIn('color', context.exception.message_dict)

    def test_too_long_color(self):
        """Test too long color raises validation error"""
        group = LayerGroup(
            proyecto=self.project,
            nombre='Test Group',
            color='#FF57333'
        )
        with self.assertRaises(ValidationError) as context:
            group.full_clean()
        self.assertIn('color', context.exception.message_dict)

    def test_empty_color(self):
        """Test empty color uses default"""
        group = LayerGroup.objects.create(
            proyecto=self.project,
            nombre='Test Group',
            color=''
        )
        # Empty string should use default
        self.assertEqual(group.color, '')

    def test_color_with_spaces(self):
        """Test color with spaces raises validation error"""
        group = LayerGroup(
            proyecto=self.project,
            nombre='Test Group',
            color='# FF5733'
        )
        with self.assertRaises(ValidationError) as context:
            group.full_clean()
        self.assertIn('color', context.exception.message_dict)

    def test_update_color(self):
        """Test updating color field"""
        group = LayerGroup.objects.create(
            proyecto=self.project,
            nombre='Test Group',
            color='#FF5733'
        )
        group.color = '#00FF00'
        group.save()
        group.refresh_from_db()
        self.assertEqual(group.color, '#00FF00')

    def test_color_persists_after_save(self):
        """Test color persists correctly after save"""
        group = LayerGroup.objects.create(
            proyecto=self.project,
            nombre='Test Group',
            color='#123ABC'
        )
        group_id = group.id

        # Retrieve from database
        retrieved_group = LayerGroup.objects.get(id=group_id)
        self.assertEqual(retrieved_group.color, '#123ABC')
