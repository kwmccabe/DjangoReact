import React, { useState } from 'react';
// import axios from 'axios';

// usage:
// import APIPost from './APIPost';
// const { handleSubmit, validated, status, message } = APIPost({xtraData,});
//

export default function APIPost({ additionalData, endpointUrl }) {
    const debug = false;  // console logging

    const [validated, setValidated] = useState(false);
    const [status, setStatus] = useState("");
    const [message, setMessage] = useState("");

    const handleSubmit = (e) => {
        const form = e.currentTarget;
        if (form) {
            e.preventDefault();
            setStatus("loading");
            setMessage("");
            if (debug) console.log("APIPost::handleSubmit : form.elements=", form.elements);

            const valid = form.checkValidity();
            setValidated(true);
            if (valid === false) {
                e.stopPropagation();
                setStatus("invalid");
                //setMessage("Validation error.");
                return;
            }

            const data = Array.from(form.elements)
                .filter((input) => input.name)
                .filter((input) => (input.type != "radio" || input.checked == true))
                .reduce(
                    (obj, input) => Object.assign(obj, { [input.name]: input.value }), {}
                );
            if (additionalData) {
                Object.assign(data, additionalData);
            }
            if (debug) console.log("APIPost::handleSubmit : data=", JSON.stringify(data));

            const finalFormEndpoint = endpointUrl || form.action;
            fetch(finalFormEndpoint, {
                method: "POST",
                mode: "cors",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            })
            .then((response) => {
                //if (debug) console.log("APIPost::handleSubmit : response=", response);
                if (response.status !== 200) {
                    throw new Error(response.statusText);
                }
                return response.json();
            })
            .then((json) => {
                if (debug) console.log("APIPost::handleSubmit : json=", json);
                setStatus("success");
                setMessage("Form Submitted");
            })
            .catch((err) => {
                console.log("APIPost::handleSubmit : error=", err)
                setStatus("error");
                setMessage(err.toString());
            });
        }
        if (debug) console.log("APIPost::handleSubmit: status=", status, " message=", message);
    };

    return { handleSubmit, validated, status, message };
}
