import React, { useState, useEffect } from 'react';
import { Form, Button, Row, Col } from 'react-bootstrap';
import { Container } from 'react-bootstrap';
import '../styles/NewsCreatePage.scss';
import HwpDataProcessor from './HwpDataProcessor';

const NewsCreatePage = ({ addNewsItem }) => {
  const today = new Date().toISOString().split('T')[0];

  const [formData, setFormData] = useState({
    creationDate: today,
    updateDate: today,
    category1: '',
    category2: '',
    category3: '',
    category4: '',
    author: '',
    editor: '',
    title: '',
    subtitle: '',
    content: '',
    image: '',
    status: ''
  });

  const [categories, setCategories] = useState({
    category1: [],
    category2: [],
    category3: [],
    category4: []
  });

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/categories');
        if (!response.ok) throw new Error('Failed to fetch categories');
        const data = await response.json();
        console.log('Fetched categories:', data);
        setCategories({
          category1: data[0].category1 || [],
          category2: data[0].category2 || [],
          category3: data[0].category3 || [],
          category4: data[0].category4 || []
        });
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    };

    fetchCategories();
  }, []);

  const handleHwpData = (processedData) => {
    setFormData({
      ...formData,
      title: processedData.title || '',
      subtitle: processedData.subtitle || '',
      content: processedData.content || '',
      image: processedData.image || ''
    });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleImageChange = async (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await fetch('http://localhost:5000/upload/image', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Image upload failed');
      }

      const data = await response.json();
      setFormData((prevFormData) => ({ ...prevFormData, image: data.imageUrl }));
    } catch (error) {
      console.error('Error uploading image:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Form submitted', formData);
    try {
      const response = await fetch('http://localhost:5000/news', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        console.error('Error:', await response.text());
        return;
      }

      const data = await response.json();
      console.log('Success:', data);
      addNewsItem(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleAutoFill = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/process-hwp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      });

      if (!response.ok) {
        throw new Error('Failed to auto-fill data');
      }

      const data = await response.json();
      setFormData((prevData) => ({
        ...prevData,
        title: data.title,
        subtitle: data.subtitle,
        content: data.content,
      }));
    } catch (error) {
      console.error('Error auto-filling data:', error);
    }
  };

  return (
    <Container>
      <HwpDataProcessor onProcessed={handleHwpData} />
      <Button onClick={handleAutoFill}>자동 채우기</Button>
      <Form onSubmit={handleSubmit}>
        <Row className="mb-3">
          {Object.keys(categories).map((key, index) => (
            <Col xs={12} md={6} key={key}>
              <Form.Group controlId={`form${key}`}>
                <Form.Label>{`카테고리${index + 1}`}</Form.Label>
                <Form.Control as="select" name={key.slice(0, -7)} value={formData[key.slice(0, -7)]} onChange={handleChange}>
                  <option value="">선택하세요</option>
                  {Array.isArray(categories[key]) && categories[key].map((option) => (
                    <option key={option.id} value={option.id}>{option.name}</option>
                  ))}
                </Form.Control>
              </Form.Group>
            </Col>
          ))}
        </Row>
        <Form.Group controlId="formTitle">
          <Form.Label>제목</Form.Label>
          <Form.Control type="text" placeholder="제목 입력" name="title" value={formData.title} onChange={handleChange} />
        </Form.Group>
        <Form.Group controlId="formSubtitle">
          <Form.Label>부제목</Form.Label>
          <Form.Control type="text" placeholder="부제목 입력" name="subtitle" value={formData.subtitle} onChange={handleChange} />
        </Form.Group>
        <Form.Group controlId="formContent">
          <Form.Label>내용</Form.Label>
          <Form.Control as="textarea" rows={5} name="content" value={formData.content} onChange={handleChange} />
        </Form.Group>
        <Form.Group controlId="formImage">
          <Form.Label>이미지 업로드</Form.Label>
          <Form.Control type="file" onChange={handleImageChange} />
        </Form.Group>
        <Button variant="primary" type="submit">저장</Button>
      </Form>
    </Container>
  );
};

export default NewsCreatePage;
