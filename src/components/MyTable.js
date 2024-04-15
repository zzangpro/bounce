import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Table, Form, FormControl, Button, Row, Col } from 'react-bootstrap';

import '../styles/MyTable.scss'; // 이 파일 내에 해당하는 스타일을 정의해야 함

const MyTable = ({ data }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const navigate  = useNavigate();
  const handleRegisterClick = () => {
    navigate('/create-news'); // "등록" 버튼 클릭 시 '/create-news'로 이동
  };

  // 임시로 테이블의 데이터를 생성합니다. 실제로는 서버로부터 받아온 데이터를 사용합니다.

   // 검색 기능: 입력된 검색어에 따라 데이터 필터링
   const filteredData = searchTerm
  ? data.filter(item =>
      item.title.toLowerCase().includes(searchTerm.toLowerCase())
    )
  : data;


  return (
    <div className="table-container">
       <Row className="justify-content-between mb-3">
        <Col md="auto">
         <Button variant="primary" onClick={handleRegisterClick}>등록</Button>
        </Col>
        <Col md="auto">
          <Form className="d-flex">
            <FormControl 
              type="text" 
              placeholder="Search" 
              className="mr-sm-2" 
              onChange={e => setSearchTerm(e.target.value)} 
            />
            <Button variant="outline-success">Search</Button>
          </Form>
      </Col>
      </Row>
      <Table striped bordered hover>
          <thead>
            <tr>
              <th>#</th>
              <th>소속</th>
              <th>입력일</th>
              <th>수정일</th>
              <th>제목</th>
              <th>글쓴이</th>
              <th>편집자</th>
              <th>분류1</th>
              <th>분류2</th>
              <th>분류3</th>
              <th>분류4</th>
              <th>이미지</th>
              <th>상태</th>
            </tr>
          </thead>
        <tbody>
         {filteredData.map((item, index) => (
            <tr key={index}>
              <td><input type="checkbox" /></td>
              <td>{item.affiliation}</td>
              <td>{item.creationDate}</td>
              <td>{item.updateDate}</td>
              <td>{item.title}</td>
              <td>{item.author}</td>
              <td>{item.editor}</td>
              <td>{item.category1}</td>
              <td>{item.category2}</td>
              <td>{item.category3}</td>
              <td>{item.category4}</td>
              <td>{item.image}</td>
              <td>{item.status}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default MyTable;