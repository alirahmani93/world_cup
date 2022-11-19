import http from 'k6/http';
import {check, sleep} from 'k6';
import {Counter, Gauge, Rate, Trend} from 'k6/metrics';

function makeid(length) {
    let result = '09';
    let characters = '0123456789';
    let charactersLength = characters.length;
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

function makeUsername(length) {
    let result = '';
    let characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let charactersLength = characters.length;
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

console.log('___________________________________________________');

const myCounter = new Counter('my_counter');  // A metric that cumulatively sums added values.
const myGauge = new Counter('my_gauge');      // A metric that stores the min, max and last values added to it.
const myRate = new Counter('my_rate');        // A metric that tracks the percentage of added values that are non-zero.
const myTrend = new Counter('my_trend');      // A metric that allows for calculating statistics on the added values (min, max, average and percentiles).

const baseUrl = "http://79.175.131.40:8000"

let settings = [

     {
         "url": baseUrl + '/api/football/match/',
         "method": "GET",
         "timeout": 0,
         "headers": null,
     },
     {
         "url": baseUrl + '/api/football/match/',
         "method": "GET",
         "timeout": 0,
         "headers": null,
     },
     {
         "url": baseUrl + '/api/football/team/?with_player=True',
         "method": "GET",
         "timeout": 0,
         "headers": null,
     },
    {
        "url": baseUrl + "/api/common/configuration/",
        "method": "GET",
        "timeout": 0,
        "headers": null,
    },
     {
         "url": baseUrl + "/api/player/login/",
         "method": "POST",
         "timeout": 5,
         "headers": {
             "Content-Type": "application/json"
         },
         "data": JSON.stringify({ // data registered from sso
             "id": makeid(9),  // add your player id
             "username": makeUsername(6), // add your username
         }),
     },
     {
         "url": baseUrl + "/api/player/leaderboard/",
         "method": "GET",
         "timeout": 0,
         "headers": null,
         "data": null,
     },
];

function consoleStatusMessage(result) {
    var prefix = 'status is: '

    if (result.status == 200) {
        myRate.add(true)
        console.log(prefix + "OK")
    } else if (result.status == 201) {
        myRate.add(true)
        console.log(prefix + "Created")
    } else if (result.status == 400) {
        myRate.add(false)
        console.log(prefix + "Bad Request")
    } else if (result.status == 401) {
        myRate.add(false)
        console.log(prefix + "Unauthorized")
    } else if (result.status == 403) {
        myRate.add(false)
        console.log(prefix + "Forbidden")
    } else if (result.status == 404) {
        myRate.add(false)
        console.log(prefix + "Not Found")
    } else if (result.status == 500) {
        myRate.add(false)
        console.log(prefix + "Server Error")
    } else {
        myRate.add(false)
        console.log(prefix + result.status)
    }
}

function CheckResultStatus(result) {
    check(result, {
            'is tls version': (r) => r.tls_version === 'tls1.2',
            'is proto HTTP/2.0': (r) => r.proto === 'HTTP/2.0',
            'is status 200': (r) => r.status === 200,
            'is status 201': (r) => r.status === 201,
            'is status 400': (r) => r.status === 400,
            'is status 401': (r) => r.status === 401,
            'is status 403': (r) => r.status === 403,
            'is status 404': (r) => r.status === 404,
            'is status 405': (r) => r.status === 405,
            'is status 500': (r) => r.status === 500,
        },
        {myTag: 'hola'} // define a threshold based on a particular check or group of checks.
    );
};

function SendRequest(item, url, payload, params) {
    var result = null

    if (item.method == "GET") {
       // console.log('>>>>A')
        result = http.get(url, payload, params);
    } else if (item.method == "POST") {
        result = http.post(url, payload, params);
    } else if (item.method == "PUT") {
        result = http.put(url, payload, params);
    } else {
        console.log("Method Not Found");
    }
    return result
};

export const option = {
//    vus: 100,
//    duration: '2s',

    stages: [
        {duration: '5m', target: 60}, // simulate ramp-up of traffic from 1 to 60 users over 5 minutes.
        {duration: '10m', target: 60}, // stay at 60 users for 10 minutes
        {duration: '3m', target: 100}, // ramp-up to 100 users over 3 minutes (peak hour starts)
        {duration: '2m', target: 100}, // stay at 100 users for short amount of time (peak hour)
        {duration: '3m', target: 60}, // ramp-down to 60 users over 3 minutes (peak hour ends)
        {duration: '10m', target: 60}, // continue at 60 for additional 10 minutes
        {duration: '5m', target: 0}, // ramp-down to 0 users
    ],

    'thresholds': {
        'checks{myTag:hola}': ['rate>0.9'],
        checks: ['rate>0.9'],
        http_req_failed: ['rate<0.01'], // http errors should be less than 1%
        http_req_duration: ['p(90) < 400', 'p(95) < 800', 'p(99.9) < 2000'], //ex. 95% of requests should be below 800ms
        http_req_tls_handshaking: [
            {
                threshold: 'p(90) < 10',
                abortOnFail: true,
                delayAbortEval: '1s',
            }
        ],
    }
};

 export default function () {
     myGauge.add(1);
     myGauge.add(2);
     myTrend.add(1);
     myTrend.add(4);

     for (let i = 0; i < settings.length; i++) {
         myCounter.add(1);
         let item = settings[i]
         console.log(item.url)

         const url = item.url;
         const payload = item.data;

         const params = {
             headers: item.headers,
        };
         // console.log(url,payload,params)
         var result = SendRequest(item, url, payload, params)
         CheckResultStatus(result)
         consoleStatusMessage(result)
         // console.log(result)
// //        sleep(1);
     }
 };
