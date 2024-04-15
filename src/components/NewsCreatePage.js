import React, { useState } from 'react';
import { Form, FormControl, Button, Row, Col, InputGroup } from 'react-bootstrap';
import { Container } from 'react-bootstrap';
import '../styles/NewsCreatePage.scss'; // 이 파일 내에 해당하는 스타일을 정의해야 함
//import { addNews } from '../api/newsAPI'; // API 호출 함수 임포트

const NewsCreatePage = ({ addNewsItem }) => {
  // 현재 날짜를 YYYY-MM-DD 형식으로 초기화
  const today = new Date().toISOString().split('T')[0];
  
  const submitNewsItem = async (newsItem) => {
    try {
        const response = await fetch('http://localhost:3000/news', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newsItem),
        });

        if (!response.ok) {
            throw new Error('Something went wrong');
        }

        const data = await response.json();
        console.log('Success:', data);
        // 여기에서 추가 처리를 할 수 있습니다...
    } catch (error) {
        console.error('Error:', error);
    }
};

  // 상태 관리
  const [formData, setFormData] = useState({
    creationDate: today, // 현재 날짜
    updateDate: today, // 업데이트 날짜도 추가해야 할 수 있음
    category1: '', // 선택된 값
    category2: '', // 선택된 값
    category3: '', // 선택된 값
    category4: '', // 선택된 값
    author: '', // 입력된 값
    editor: '', // 입력된 값
    title: '', // 입력된 제목
    subtitle: '', // 입력된 부제목, `MyTable`에서 사용하지 않는다면 제외해도 됨
    content: '', // 입력된 내용, `MyTable`에서 사용하지 않는다면 제외해도 됨
    image: '', // 업로드된 이미지 정보
    status: '' // 상태 정보, 필요에 따라 추가
  });

  // 입력 핸들러
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // 이미지 업로드 핸들러
  const handleImageChange = (e) => {
    // 파일 리더를 사용하여 이미지를 Base64로 인코딩합니다.
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onloadend = () => {
      setFormData({ ...formData, image: reader.result });
    };
    reader.readAsDataURL(file);
  };

  // 저장 핸들러
  const handleSubmit = (e) => {
    e.preventDefault();
    // addNewsItem 함수를 호출하여 상위 컴포넌트로 데이터 전달
    console.log('Form submitted', formData);
    addNewsItem(formData);
    // 폼 초기화 또는 페이지 이동 등 추가 작업을 수행할 수 있습니다.
  };

  return (
    <Container>
      <Form onSubmit={handleSubmit}>
        <Row className="mb-3">
          <Col xs={12} md={6}>
            <Form.Group controlId="formCategory1">
              <Form.Label>카테고리1</Form.Label>
              <Form.Control as="select" name="category1" value={formData.category1} onChange={handleChange}>
                <option value="">선택하세요</option>
                {/* 카테고리 옵션을 동적으로 렌더링 */}
              </Form.Control>
            </Form.Group>
          </Col>

           {/* 카테고리2 드롭다운 */}
           <Col xs={12} md={6}>
            <Form.Group controlId="formCategory2">
              <Form.Label>카테고리2</Form.Label>
              <Form.Control as="select" name="category2" value={formData.category2} onChange={handleChange}>
                <option value="">선택하세요</option>
                {/* 카테고리2 옵션 여기에 추가 */}
              </Form.Control>
            </Form.Group>
          </Col>

          {/* 카테고리3 드롭다운 */}
          <Col xs={12} md={6}>
            <Form.Group controlId="formCategory3">
              <Form.Label>카테고리3</Form.Label>
              <Form.Control as="select" name="category3" value={formData.category3} onChange={handleChange}>
                <option value="">선택하세요</option>
                {/* 카테고리3 옵션 여기에 추가 */}
              </Form.Control>
            </Form.Group>
          </Col>

          {/* 카테고리4 드롭다운 */}
          <Col xs={12} md={6}>
            <Form.Group controlId="formCategory4">
              <Form.Label>카테고리4</Form.Label>
              <Form.Control as="select" name="category4" value={formData.category4} onChange={handleChange}>
                <option value="">선택하세요</option>
                {/* 카테고리4 옵션 여기에 추가 */}
              </Form.Control>
            </Form.Group>
          </Col>
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
