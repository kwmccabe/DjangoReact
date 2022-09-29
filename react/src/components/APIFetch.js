import React, { useEffect, useState } from 'react';
// import axios from 'axios';

// usage:
// import APIFetch from './APIFetch';
// const [data, loading, error] = APIFetch(fetch_url);
//

export default function APIFetch(url, opts) {
    const debug = false;  // console logging

    const [data, setData] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(false)

//     opts = {
//         headers : {
//             'Content-Type': 'application/json',
//             'Accept': 'application/json'
//         }
//     }

    useEffect(() => {
        if (debug) console.log("APIFetch::useEffect : url=",url);
        setLoading(true);
        fetch(url, opts)
            .then((response) => {
                if (debug) console.log("APIFetch::useEffect : response=",response);
                return response.json();
            })
            .then((json) => {
                if (debug) console.log("APIFetch::useEffect : json=",json);
                setData(json);
            })
            .catch((err) => {
                console.log("APIFetch::useEffect : error=",err);
                setError(err.toString())
            });
        setLoading(false)
    }, [ url ]);

    return [ data, loading, error ]
}
