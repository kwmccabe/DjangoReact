// import React from 'react';

import {
  useParams,
} from "react-router-dom";

import {
    Button,
    Form,
} from 'react-bootstrap';

import APIFetch from './APIFetch';
import APIPost from './APIPost';

export default function Vote() {
    let { pollId } = useParams();
    let fetch_url = "http://127.0.0.1:8000/api/polls/"+pollId;
    let post_url = "http://127.0.0.1:8000/api/polls/"+pollId+"/submitvote/";
    const [data, loading, error] = APIFetch(fetch_url);

    const xtraData = {sent: new Date().toISOString(),};
    const { handleSubmit, validated, status, message } = APIPost({xtraData,});

    if (status === "success") {
        return (
        <>
            <div>Thank you!</div>
            <div>{message}</div>
        </>
        );
    }
//
//     if (status === "error") {
//         return (
//         <>
//             <div>Something bad happened!</div>
//             <div>{message}</div>
//         </>
//         );
//     }

    return (
    <>
        { loading && <p>LOADING</p> }
        { error && <p>ERROR : {error}</p> }
        { status && <p>STATUS : {status}</p> }
        { message && <p>MESSAGE : {message}</p> }
        { (data && data.id) && (
            <>
                <h3>{ data.poll_title } ({ data.id })</h3>
                <p>fetch: {fetch_url}</p>
                <hr />
                <Form noValidate validated={validated}
                        action={post_url}
                        onSubmit={handleSubmit}
                        method="POST"
                        target="_blank"
                    >
                    <VoteQuestions data={data.question_set} />
                    <Button variant="primary" type="submit">Submit</Button>
                </Form>
                <hr />
                <p>FOOTER</p>
            </>
        )}
    </>
    );
}


function VoteQuestions(props) {
    return (
    <>
        {
        props.data.map( question => (
            <Form.Group className="mb-3" controlId={`question-${question.id}`} key={question.id}>
                <Form.Label>{question.question_text} ({question.question_sort},{question.id})</Form.Label>
                <VoteChoices data={question.choice_set} />
            </Form.Group>
        ))
        }
    </>
    );
}


function VoteChoices(props) {
    return (
    <>
        <Form.Control.Feedback type="invalid">Please choose one of the following.</Form.Control.Feedback>
        {
        props.data.map( choice => (
            <Form.Check required type="radio"
                label={`${choice.choice_text} (${choice.id})`}
                name={`question-${choice.question}`}
                id={`question-${choice.question}-${choice.id}`}
                value={`${choice.id}`}
                key={choice.id}
                />
        ))
        }
    </>
    );
}

