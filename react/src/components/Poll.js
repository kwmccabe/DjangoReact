// import React from 'react';

import {
  useParams,
} from "react-router-dom";

import APIFetch from './APIFetch';


export default function Poll() {
    let { pollId } = useParams();
    let fetch_url = "http://127.0.0.1:8000/api/polls/"+pollId;
    const [data, loading, error] = APIFetch(fetch_url);

    return (
    <>
        <h2>{ (data) ? data.poll_title : 'Poll' }</h2>
        { loading && <p>LOADING</p> }
        { error && <p>ERROR : {error}</p> }
        <p>fetch: {fetch_url}</p>
        <hr />
        { (data) && (
            <PollQuestions data={data.question_set} />
        )}

        <hr />
        <p>FOOTER</p>
    </>
    );
}


function PollQuestions(props) {
    return (
    <ol>
        {
        props.data.map( question => (
            <li key={question.id}>
                <span>{question.question_text}</span>
                <PollChoices data={question.choice_set} />
            </li>
        ))
        }
    </ol>
    );
}


function PollChoices(props) {
    return (
    <ol type="a">
        {
        props.data.map( choice => (
            <li key={choice.id}>{choice.choice_text} - {choice.votes} votes</li>
        ))
        }
    </ol>
    );
}
