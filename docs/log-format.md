| Поле          | Тип      | Значение      |
| ------------- | -------- | ------------- |
| timestamp     | datetime | время запроса |
| ip            | string   | IP клиента    |
| method        | string   | HTTP method   |
| path          | string   | endpoint      |
| status        | integer  | HTTP status   |
| response_time | integer  | ms            |

timestamp: ip/method, path, status; response_time
2026-08-16T10:15:32 - "10.0.0.5"/"GET", "/api/users", 200; 125
