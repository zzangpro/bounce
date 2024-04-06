import React, { useState } from 'react';
import { Navbar, Nav, NavDropdown } from 'react-bootstrap';
import '../styles/MyNavbar.scss'; // 이 파일 내에 해당하는 스타일을 정의해야 함

const MyNavbar = () => {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="navbar-container"> {/* 이 div 태그로 네비게이션 바를 감쌉니다 */}
      <Navbar expanded={expanded} expand="lg" bg="red" variant="dark" fixed="left">
        <Navbar.Brand href="#home"><img src="logo.png" width="200" height="50" className="d-inline-block align-top" alt="" />
        </Navbar.Brand>
        <Navbar.Toggle onClick={() => setExpanded(expanded ? false : "expanded")} aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="flex-column">
            <NavDropdown title="설정 관리" id="nav-dropdown1">
              <NavDropdown.Item href="#action/1.1">코드 관리</NavDropdown.Item>
              <NavDropdown.Item href="#action/1.2">소속 관리</NavDropdown.Item>
              <NavDropdown.Item href="#action/1.3">기사 발송 통계</NavDropdown.Item>
              <NavDropdown.Item href="#action/1.4">전송업체 관리</NavDropdown.Item>
              <NavDropdown.Item href="#action/1.5">전송업체 관리_US</NavDropdown.Item>
              <NavDropdown.Item href="#action/1.6">리뉴얼기사 관리</NavDropdown.Item>
              {/* 추가 하위 카테고리 */}
            </NavDropdown>
            <NavDropdown title="관리자 관리" id="nav-dropdown2">
              <NavDropdown.Item href="#action/2.1">관리자목록</NavDropdown.Item>
              {/* 하위 카테고리 */}
            </NavDropdown>
            <NavDropdown title="보도자료" id="nav-dropdown3">
              <NavDropdown.Item href="/create-news">보도자료 등록_ROK</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.2">보도자료 등록_US</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.3">단어 관리</NavDropdown.Item>
              {/* 하위 카테고리 */}
            </NavDropdown>
            <NavDropdown title="이메일" id="nav-dropdown4">
             <NavDropdown.Item href="#action/4.1">가져온 이메일</NavDropdown.Item>
             <NavDropdown.Item href="#action/4.2">사용한 이메일</NavDropdown.Item>


              {/* 하위 카테고리 */}
            </NavDropdown>
            <NavDropdown title="거래처 관리" id="nav-dropdown5">
              <NavDropdown.Item href="#action/5.1">전체 현황</NavDropdown.Item>
              <NavDropdown.Item href="#action/5.2">사용중</NavDropdown.Item>
              <NavDropdown.Item href="#action/5.3">해지</NavDropdown.Item>
              {/* 하위 카테고리 */}
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    </div>

  );
};

export default MyNavbar;
