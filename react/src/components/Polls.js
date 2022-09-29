// import React from 'react';

import { generatePath } from "react-router";
import {
  Link,
  Outlet,
} from "react-router-dom";

import APIFetch from './APIFetch';


export default function Polls() {
    const fetch_url = "http://127.0.0.1:8000/api/listpolls";
    const [data, loading, error] = APIFetch(fetch_url);

    return (
    <>
        <h2>Polls</h2>
        { loading && <p>LOADING</p> }
        { error && <p>ERROR : {error}</p> }
        <p>fetch: {fetch_url}</p>
        <hr />
        { (data && data.length == 0) && <p>NO POLLS</p> }
        { (data && data.length > 0) && (
            <div className="row">
            {
            data.map( poll => (
                <div key={poll.id} className="col-4">
                    <div className="card mb-3">
                        <div className="card-body">
                            <h5 className="card-title">{poll.poll_title}</h5>
                            <p className="card-text">{poll.cnt_questions} Questions</p>
                        </div>
                        <div className="card-body text-center">
                            <Link to={generatePath("/polls/:id/vote/", { id: poll.id, })}>Vote</Link>
                            |
                            <Link to={generatePath("/polls/:id/", { id: poll.id, })}>Show Results</Link>
                        </div>
                    </div>
                </div>
            ))
            }
            </div>
        )}

{/* <Outlet /> : if nested route(s) */}

        <hr />
        <p>FOOTER</p>
    </>
    );
}
