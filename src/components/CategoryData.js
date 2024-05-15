// src/components/CategoryData.js
import React, { useEffect } from 'react';
import { fetchAllCategories } from '../utils/categoryAPI'; // 경로를 올바르게 설정

const CategoryData = ({ onCategoriesLoaded }) => {
  useEffect(() => {
    fetchAllCategories().then(categories => {
      onCategoriesLoaded(categories);
    }).catch(error => {
      console.error('Failed to fetch categories', error);
    });
  }, [onCategoriesLoaded]);

  return null; // 이 컴포넌트는 UI를 렌더링하지 않고, 데이터 로딩만 수행합니다.
};

export default CategoryData;
