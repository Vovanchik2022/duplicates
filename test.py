from tkinter import Image
import unittest
from unittest.mock import patch
from main import load_images_from_folder, find_duplicates, print_duplicates

class TestImageProcessing(unittest.TestCase):
    @patch('main.os.listdir')
    @patch('main.Image.open')
    def test_load_images_from_folder(self, mock_open, mock_listdir):
        mock_listdir.return_value = ['image1.jpg', 'image2.png', 'text.txt']
        mock_open.side_effect = [Image.new('RGB', (10, 10)), Image.new('RGB', (20, 20)), IOError('File not found')]

        images = load_images_from_folder('/fake/directory')

        self.assertEqual(len(images), 2)
        self.assertEqual(images[0][0], 'image1.jpg')
        self.assertEqual(images[1][0], 'image2.png')

    def test_find_duplicates(self):
        img1 = Image.new('RGB', (10, 10))
        img2 = Image.new('RGB', (10, 10))
        images = [('image1.jpg', img1), ('image2.jpg', img2)]
        
        duplicates = find_duplicates(images)
        
        self.assertEqual(len(duplicates), 1)
        self.assertIn(('image2.jpg', 'image1.jpg'), duplicates)

    @patch('builtins.print')
    def test_print_duplicates(self, mock_print):
        duplicates = [('image1.jpg', 'image2.jpg')]
        
        print_duplicates(duplicates)
        
        mock_print.assert_called_with('Дубликаты: image1.jpg и image2.jpg')

if __name__ == '__main__':
    unittest.main()
