// import React from 'react';

import {
  NavLink,
  useLocation
} from "react-router-dom";

import {
    Container,
    Nav,
    Navbar,
} from 'react-bootstrap';


// see https://react-bootstrap.github.io/components/navbar/
function SiteNav() {
    let location = useLocation();

    return (
    <Navbar bg="light" expand="lg" align="start" className="mb-3">
        <Container fluid>
            <Navbar.Brand href="/">ReactApp</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="me-auto">
{/* <Nav.Link href="/">Home</Nav.Link> */}
                    <NavLink to="polls" className="nav-link">Polls</NavLink>
                </Nav>

                <Navbar.Text className="text-end">path: {location.pathname}</Navbar.Text>
            </Navbar.Collapse>
        </Container>
    </Navbar>
);
}

export default SiteNav;
