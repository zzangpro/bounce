import React, { useState, useEffect } from 'react';
import { Form, Button, Container, Row, Col } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import '../styles/NewsCreatePage.scss';

const NewsCreatePage = () => {
  const [formData, setFormData] = useState({
    title: '',
    subtitle: '',
    content: '',
    category1: '',
    category2: '',
    category3: '',
    category4: '',
    image: null,
  });

  const [categories, setCategories] = useState({ category1: [], category2: [], category3: [], category4: [] });
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/categories');
        if (!response.ok) {
          throw new Error('Failed to fetch categories');
        }
        const data = await response.json();
        console.log('Fetched categories:', data);
  
        const categorizedData = {
          category1: data[0].category1,
          category2: data[0].category2,
          category3: data[0].category3,
          category4: data[0].category4,
        };
  
        setCategories(categorizedData);
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    };
  
    fetchCategories();
  }, []);
  

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setFormData((prevData) => ({
      ...prevData,
      image: file,
    }));
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formDataToSubmit = new FormData();
      formDataToSubmit.append('title', formData.title);
      formDataToSubmit.append('subtitle', formData.subtitle);
      formDataToSubmit.append('content', formData.content);
      formDataToSubmit.append('category1', formData.category1);
      formDataToSubmit.append('category2', formData.category2);
      formDataToSubmit.append('category3', formData.category3);
      formDataToSubmit.append('category4', formData.category4);
      if (formData.image) {
        formDataToSubmit.append('image', formData.image);
      }

      const response = await fetch('http://localhost:5000/news', {
        method: 'POST',
        body: formDataToSubmit,
      });

      if (!response.ok) {
        throw new Error('Failed to create news');
      }

      navigate('/news');
    } catch (error) {
      console.error('Error creating news:', error);
    }
  };

  return (
    <Container className="news-create-container">
      <h2>Create News</h2>
      <Row className="mb-3">
        <Col>
          <Button variant="secondary" onClick={handleAutoFill}>Auto Fill</Button>
        </Col>
      </Row>
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="formCategory1">
          <Form.Label>Category 1</Form.Label>
          <Form.Control
            as="select"
            name="category1"
            value={formData.category1}
            onChange={handleChange}
          >
            <option value="">Select a category</option>
            {categories.category1.map((category, index) => (
              <option key={index} value={category.name}>{category.name}</option>
            ))}
          </Form.Control>
        </Form.Group>
        <Form.Group controlId="formCategory2">
          <Form.Label>Category 2</Form.Label>
          <Form.Control
            as="select"
            name="category2"
            value={formData.category2}
            onChange={handleChange}
          >
            <option value="">Select a category</option>
            {categories.category2.map((category, index) => (
              <option key={index} value={category.name}>{category.name}</option>
            ))}
          </Form.Control>
        </Form.Group>
        <Form.Group controlId="formCategory3">
          <Form.Label>Category 3</Form.Label>
          <Form.Control
            as="select"
            name="category3"
            value={formData.category3}
            onChange={handleChange}
          >
            <option value="">Select a category</option>
            {categories.category3.map((category, index) => (
              <option key={index} value={category.name}>{category.name}</option>
            ))}
          </Form.Control>
        </Form.Group>
        <Form.Group controlId="formCategory4">
          <Form.Label>Category 4</Form.Label>
          <Form.Control
            as="select"
            name="category4"
            value={formData.category4}
            onChange={handleChange}
          >
            <option value="">Select a category</option>
            {categories.category4.map((category, index) => (
              <option key={index} value={category.name}>{category.name}</option>
            ))}
          </Form.Control>
        </Form.Group>

        <Form.Group controlId="formTitle">
          <Form.Label>Title</Form.Label>
          <Form.Control
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            placeholder="Enter the news title"
          />
        </Form.Group>
        <Form.Group controlId="formSubtitle">
          <Form.Label>Subtitle</Form.Label>
          <Form.Control
            type="text"
            name="subtitle"
            value={formData.subtitle}
            onChange={handleChange}
            placeholder="Enter the news subtitle"
          />
        </Form.Group>
        <Form.Group controlId="formContent">
          <Form.Label>Content</Form.Label>
          <Form.Control
            as="textarea"
            rows={10}
            name="content"
            value={formData.content}
            onChange={handleChange}
            placeholder="Enter the news content"
          />
        </Form.Group>
        <Form.Group controlId="formImage">
          <Form.Label>Image</Form.Label>
          <Form.Control
            type="file"
            name="image"
            onChange={handleFileChange}
          />
        </Form.Group>
        <Button variant="primary" type="submit" className="mt-3">
          Submit
        </Button>
      </Form>
    </Container>
  );
};

export default NewsCreatePage;
