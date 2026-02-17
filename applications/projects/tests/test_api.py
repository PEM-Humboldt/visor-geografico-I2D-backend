"""
Integration tests for LayerGroup API with color field
"""
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from applications.projects.models import Project, LayerGroup


class LayerGroupColorAPITests(APITestCase):
    """Test cases for LayerGroup API color functionality"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.project = Project.objects.create(
            nombre_corto='test',
            nombre='Test Project',
            coordenada_central_x=-74.0,
            coordenada_central_y=4.0
        )
        self.group = LayerGroup.objects.create(
            proyecto=self.project,
            nombre='Test Group',
            color='#FF5733'
        )

    def test_get_layer_group_includes_color(self):
        """Test GET returns color field"""
        url = f'/api/layer-groups/{self.group.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('color', response.data)
        self.assertEqual(response.data['color'], '#FF5733')

    def test_list_layer_groups_includes_color(self):
        """Test LIST returns color field for all groups"""
        url = '/api/layer-groups/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        self.assertIn('color', response.data[0])

    def test_create_layer_group_with_color(self):
        """Test POST creates group with color"""
        self.client.force_authenticate(user=self.user)
        url = '/api/layer-groups/'
        data = {
            'proyecto': self.project.id,
            'nombre': 'New Group',
            'color': '#00FF00',
            'orden': 1,
            'fold_state': 'close'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['color'], '#00FF00')

        # Verify in database
        group = LayerGroup.objects.get(id=response.data['id'])
        self.assertEqual(group.color, '#00FF00')

    def test_create_layer_group_with_3_digit_color(self):
        """Test POST creates group with 3-digit color"""
        self.client.force_authenticate(user=self.user)
        url = '/api/layer-groups/'
        data = {
            'proyecto': self.project.id,
            'nombre': 'New Group',
            'color': '#F57',
            'orden': 1,
            'fold_state': 'close'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['color'], '#F57')

    def test_create_layer_group_without_color_uses_default(self):
        """Test POST without color uses default"""
        self.client.force_authenticate(user=self.user)
        url = '/api/layer-groups/'
        data = {
            'proyecto': self.project.id,
            'nombre': 'New Group',
            'orden': 1,
            'fold_state': 'close'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['color'], '#e3e3e3')

    def test_update_layer_group_color(self):
        """Test PUT updates color"""
        self.client.force_authenticate(user=self.user)
        url = f'/api/layer-groups/{self.group.id}/'
        data = {
            'proyecto': self.project.id,
            'nombre': 'Test Group',
            'color': '#0000FF',
            'orden': 0,
            'fold_state': 'close'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['color'], '#0000FF')

        # Verify in database
        self.group.refresh_from_db()
        self.assertEqual(self.group.color, '#0000FF')

    def test_partial_update_layer_group_color(self):
        """Test PATCH updates only color"""
        self.client.force_authenticate(user=self.user)
        url = f'/api/layer-groups/{self.group.id}/'
        data = {'color': '#ABCDEF'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['color'], '#ABCDEF')

        # Verify other fields unchanged
        self.group.refresh_from_db()
        self.assertEqual(self.group.nombre, 'Test Group')
        self.assertEqual(self.group.color, '#ABCDEF')

    def test_invalid_color_returns_error(self):
        """Test invalid color returns 400"""
        self.client.force_authenticate(user=self.user)
        url = '/api/layer-groups/'
        data = {
            'proyecto': self.project.id,
            'nombre': 'New Group',
            'color': 'invalid',
            'orden': 1,
            'fold_state': 'close'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('color', response.data)

    def test_color_without_hash_returns_error(self):
        """Test color without # returns 400"""
        self.client.force_authenticate(user=self.user)
        url = '/api/layer-groups/'
        data = {
            'proyecto': self.project.id,
            'nombre': 'New Group',
            'color': 'FF5733',
            'orden': 1,
            'fold_state': 'close'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('color', response.data)

    def test_invalid_hex_characters_returns_error(self):
        """Test invalid hex characters return 400"""
        self.client.force_authenticate(user=self.user)
        url = '/api/layer-groups/'
        data = {
            'proyecto': self.project.id,
            'nombre': 'New Group',
            'color': '#GG5733',
            'orden': 1,
            'fold_state': 'close'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('color', response.data)

    def test_wrong_length_color_returns_error(self):
        """Test wrong length color returns 400"""
        self.client.force_authenticate(user=self.user)
        url = '/api/layer-groups/'
        data = {
            'proyecto': self.project.id,
            'nombre': 'New Group',
            'color': '#FF57',  # 4 digits
            'orden': 1,
            'fold_state': 'close'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('color', response.data)

    def test_color_normalization_to_uppercase(self):
        """Test color is normalized to uppercase"""
        self.client.force_authenticate(user=self.user)
        url = '/api/layer-groups/'
        data = {
            'proyecto': self.project.id,
            'nombre': 'New Group',
            'color': '#ff5733',
            'orden': 1,
            'fold_state': 'close'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['color'], '#FF5733')

    def test_filter_by_project_includes_color(self):
        """Test filtering by project includes color"""
        url = f'/api/layer-groups/?project={self.project.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        self.assertIn('color', response.data[0])

    def test_nested_serialization_includes_color(self):
        """Test nested serialization in project detail includes color"""
        url = f'/api/projects/{self.project.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('layer_groups', response.data)
        if len(response.data['layer_groups']) > 0:
            self.assertIn('color', response.data['layer_groups'][0])

    def test_unauthenticated_cannot_create(self):
        """Test unauthenticated user cannot create"""
        url = '/api/layer-groups/'
        data = {
            'proyecto': self.project.id,
            'nombre': 'New Group',
            'color': '#00FF00',
            'orden': 1,
            'fold_state': 'close'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_can_read(self):
        """Test unauthenticated user can read"""
        url = f'/api/layer-groups/{self.group.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('color', response.data)
