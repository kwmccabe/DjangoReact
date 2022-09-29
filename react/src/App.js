// import React from 'react';

// see https://reactrouter.com/
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";

import SiteNav  from './components/SiteNav';
import Home     from './components/Home';
import Polls    from './components/Polls';
import Poll     from './components/Poll';
import Vote     from './components/Vote';


export default function App() {
    return (
    <Router>
        <SiteNav />
        <div id="main" className="container-fluid">
            <div className="row">
                <div id="content" className="col-md-12">

        <Routes>
            <Route path="" element={<Home />} />
            <Route path="polls" element={<Polls />} />
            <Route path="polls/:pollId" element={<Poll />} />
            <Route path="polls/:pollId/vote" element={<Vote />} />
        </Routes>

                </div>
            </div>
        </div>
    </Router>
    );
}

