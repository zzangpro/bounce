// src/utils/categoryAPI.js

export const fetchAllCategories = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/categories');
    if (!response.ok) throw new Error('Network response was not ok');
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch categories:', error);
    throw error;
  }
};
