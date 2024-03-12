## Spis treści

- [Spis treści](#spis-treści)
- [Cel projektu](#cel-projektu)
- [Dowód koncepcji](#dowód-koncepcji)
  - [ING](#ing)
  - [mbank](#mbank)
  - [PKO BP](#pko-bp)
- [Wnioski](#wnioski)

<div style="page-break-after: always;"></div>

## Cel projektu

Celem projektu jest stworzenie aplikacji webowej, która umożliwi użytkownikowi łączenie danych z wszystkich jego kont bankowych w jednym miejscu w celu przeglądania danych i ich analizy.

## Dowód koncepcji

Projekt opiera się głównie na obszarze bankowości, gdzie dostęp do danych jest bardzo wrażliwy, a banki są ograniczone przez liczne dyrektywy i zasady narzucone przez państwa oraz Unię Europejską. Jedną z tych dyrektyw, która okazuje się niezwykle przydatna dla takich projektów, jest dyrektywa PSD2 (Payment Services Directive). Dzięki niej banki udostępniają swoje interfejsy API wraz z danymi testowymi, aby zachęcić niezależnych deweloperów do tworzenia własnych projektów opartych na rozwiązaniach fintechowych.

Aby udowodnić możliwość stworzenia projektu, wybrałem trzy banki, dla których zebrałem informacje na temat możliwości ich interfejsów API w trybie sandbox oraz wszelkie niezbędne dokumentacje.

Jak się szybko okazało, format działania środowiska testowego trzyma się standardu we wszystkich przypadkach, gdzie banki dostarczają zestaw certyfikatów testowych oraz gotowych przykładowych skryptów bashowych. Możemy je pobrać, odpowiednio skonfigurować i uruchomić, wymieniając pomiędzy nimi uzyskane tokeny i klucze.

1. Na podstawie instrukcji musimy uruchomić pierwszy skrypt, który na podstawie certyfikatu wygeneruje dla nas `token dostępu do aplikacji`.
2. Następnie musimy skopiować `token dostępu do aplikacji` do drugiego skryptu i go uruchomić, co zwróci nam URL do strony autoryzującej nasz dostęp do konta.
3. Po wykonaniu instrukcji ze strony zostaniemy przekierowani do wybranego przez nas URL z kodem autoryzującym dla wybranego konta.
4. Na podstawie kodu autoryzującego i wcześniej uzyskanego `tokenu dostępu aplikacji` możemy wygenerować `token dostępu klienta`.
5. W naszym przypadku interesują nas interfejsy API obsługujące AIS (Accounting Information System), czyli wszystkie informacje na temat transakcji i salda naszego konta. Musimy teraz wykorzystać wcześniej zdobyte klucze, aby wysłać zapytanie do serwera, które zwróci nam wszystkie informacje zgodnie z typem zapytania.

<div style="page-break-after: always;"></div>

### ING

[Instrukcja ING](https://developer.ing.com/openbanking/resources/get-started/psd2)
[Dokumentacja ING](https://developer.ing.com/api-marketplace/marketplace/b6d5093d-626e-41e9-b9e8-ff287bbe2c07/reference?endpoint=2)

`/v3/accounts`

```json
{
  "accounts": [
    {
      "resourceId": "7de0041d-4f25-4b6c-a885-0bbeb1eab220",
      "iban": "NL69INGB0123456789",
      "name": "A. Van Dijk",
      "product": "Current Account",
      "currency": "EUR",
      "_links": {
        "balances": {
          "href": "/v2/accounts/7de0041d-4f25-4b6c-a885-0bbeb1eab220/balances"
        },
        "transactions": {
          "href": "/v2/accounts/7de0041d-4f25-4b6c-a885-0bbeb1eab220/transactions"
        }
      }
    }
  ]
}
```

`/v3/accounts/{account-id}/transactions`

```json
{
  "account": {
    "iban": "NL69INGB0123456789",
    "currency": "EUR"
  },
  "transactions": {
    "booked": [
      {
        "transactionId": "trx123456789",
        "endToEndId": "EndToEndID1234567890",
        "bookingDate": "2017-11-21",
        "valueDate": "2017-11-21",
        "executionDateTime": "2017-11-21T09:16:54.991Z",
        "amount": {
          "currency": "EUR",
          "content": 100.12
        },
        "debtorName": "Debtor Name",
        "debtorAccount": {
          "iban": "NL69INGB0123456789",
          "bban": 123456789,
          "bic": "INGBNL2A"
        },
        "transactionType": "Sepa Credit Transfer",
        "remittanceInformationUnstructured": "Unstructured remittance information example",
        "remittanceInformationStructured": {
          "type": "SCOR",
          "issuer": "ISO",
          "reference": "RF18539007547034"
        }
      }
    ],
    "info": [
      {
        "transactionId": "trx123456789",
        "endToEndId": "EndToEndID1234567890",
        "bookingDate": "2017-11-21",
        "valueDate": "2017-11-21",
        "executionDateTime": "2017-11-21T09:16:54.991Z",
        "amount": {
          "currency": "EUR",
          "content": 100.12
        },
        "debtorName": "Debtor Name",
        "debtorAccount": {
          "iban": "NL69INGB0123456789",
          "bban": 123456789,
          "bic": "INGBNL2A"
        },
        "transactionType": "Sepa Credit Transfer",
        "remittanceInformationUnstructured": "Unstructured remittance information example",
        "remittanceInformationStructured": {
          "type": "SCOR",
          "issuer": "ISO",
          "reference": "RF18539007547034"
        }
      }
    ],
    "pending": [
      {
        "transactionId": "trx987654321",
        "endToEndId": "EndToEndID1234567890",
        "bookingDate": "2017-11-21",
        "valueDate": "2017-11-21",
        "executionDateTime": "2017-11-21T09:16:54.991Z",
        "amount": {
          "currency": "EUR",
          "content": -100.12
        },
        "creditorName": "Creditor Name",
        "creditorAccount": {
          "iban": "NL69INGB0123456789",
          "bban": 123456789,
          "bic": "INGBNL2A"
        },
        "transactionType": "Sepa Credit Transfer",
        "remittanceInformationUnstructured": "Unstructured remittance information example",
        "remittanceInformationStructured": {
          "type": "SCOR",
          "issuer": "ISO",
          "reference": "RF18539007547034"
        }
      }
    ],
    "standingOrderAgreementInformation": [
      {
        "transactionAmount": {
          "amount": "100.12",
          "currency": "EUR"
        },
        "creditorAccount": {
          "iban": "NL69INGB0123456789",
          "bban": 123456789,
          "bic": "INGBNL2A"
        },
        "creditorName": "Creditor Name",
        "transactionType": "Sepa Credit Transfer",
        "remittanceInformationUnstructured": "Unstructured remittance information example",
        "additionalInformationStructured": {
          "standingOrderDetails": {
            "startDate": "2021-03-01",
            "endDate": "2021-06-31",
            "frequency": "monthly",
            "dayOfExecution": "24"
          }
        }
      }
    ],
    "_links": {
      "next": {
        "href": "/v3/accounts/7de0041d-4f25-4b6c-a885-0bbeb1eab220/transactions?next=CQR23TABC"
      }
    }
  }
}
```

<div style="page-break-after: always;"></div>

### mbank

[Dokumentacja mbank](https://developer.api.mbank.pl/documentation/api-v2#operation/getTransactionList)

`https://sandbox.api.mbank.pl/bank-simulator-pl-corpo/v2/accounts/{accountId}/transactions`

```json
{
  "transactions": [
    {
      "bookingDate": "2018-08-02",
      "transactionStatus": "DONE",
      "transactionCategory": "CREDIT",
      "aspspTransactionId": "184770007748899.010001$1533160800000",
      "amount": "111.01",
      "currency": "PLN",
      "description": "przykładowy opis transakcji",
      "transactionType": "38",
      "tradeDate": "2018-08-02",
      "auxData": {
        "txNumber": "TT1821400004"
      }
    },
    {
      "bookingDate": "2019-02-14",
      "transactionStatus": "DONE",
      "transactionCategory": "DEBIT",
      "aspspTransactionId": "186731020542100.000002$1550140901000",
      "amount": "-0.01",
      "currency": "PLN",
      "description": "przykładowy opis transakcji",
      "transactionType": "973",
      "tradeDate": "2019-02-14",
      "auxData": {
        "txNumber": "BR19045249000007",
        "customerRef": "referencje"
      }
    },
    ........
  ],
  "links": [
    {
      "rel": "nextPage",
      "href": "http://www.mbank.pl/accounts/234456-88a6-47cd-b2c4-59117f61b733/transactions?cursor=bcb62f08bff611e8a355-529269fb1459",
      "action": "GET"
    }
  ]
}
```

`https://sandbox.api.mbank.pl/bank-simulator-pl-corpo/v2/accounts`

```json
{
  "accounts": [
    {
      "accountNumber": "85114000000000000000000100",
      "accountTypeName": "",
      "accountType": {
        "code": "1001",
        "description": "Tytuł rachunku"
      }
    },
    {
      "accountNumber": "20114000000000000000000300",
      "accountTypeName": "",
      "accountType": {
        "code": "3013",
        "description": "Inny tytuł rachunku"
      }
    }
  ],
  "links": [
    {
      "rel": "nextPage",
      "href": "http://www.mbank.pl/accounts?cursor=egh62f08bff611e8a355-529269fb1467",
      "action": "GET"
    }
  ]
}
```

<div style="page-break-after: always;"></div>

### PKO BP

[Dokumentacja PKO BP](https://developers.pkobp.pl/documentation)

`https://srv-fob-sandbox.dev.k8s.inteligo.com.pl/v2_1_1.1/accounts/v2_1_1.1/getAccounts`

```json
{
  "responseHeader": {
    "requestId": "string",
    "sendDate": "2019-08-24T14:15:22Z",
    "isCallback": true
  },
  "accounts": [
    {
      "accountNumber": "string",
      "accountTypeName": "string",
      "accountType": {
        "code": "string",
        "description": "string"
      }
    }
  ],
  "pageInfo": {
    "previousPage": "string",
    "nextPage": "string"
  }
}
```

`https://srv-fob-sandbox.dev.k8s.inteligo.com.pl/v2_1_1.1/accounts/v2_1_1.1/getTransactionsDone`

```json
{
  "responseHeader": {
    "requestId": "string",
    "sendDate": "2019-08-24T14:15:22Z",
    "isCallback": true
  },
  "transactions": [
    {
      "itemId": "string",
      "amount": "string",
      "currency": "str",
      "description": "string",
      "transactionType": "string",
      "tradeDate": "2019-08-24T14:15:22Z",
      "mcc": "string",
      "auxData": {
        "property1": "string",
        "property2": "string"
      },
      "transactionCategory": "DEBIT",
      "transactionStatus": {
        "code": "string",
        "description": "string"
      },
      "initiator": {
        "value": ["string"]
      },
      "sender": {
        "accountNumber": "string",
        "accountMassPayment": "string",
        "bank": {
          "bicOrSwift": "string",
          "name": "string",
          "code": "string",
          "address": ["string"],
          "countryCode": "str"
        },
        "nameAddress": {
          "value": ["string"]
        }
      },
      "recipient": {
        "accountNumber": "string",
        "accountMassPayment": "string",
        "bank": {
          "bicOrSwift": "string",
          "name": "string",
          "code": "string",
          "address": ["string"],
          "countryCode": "str"
        },
        "nameAddress": {
          "value": ["string"]
        }
      },
      "bookingDate": "2019-08-24T14:15:22Z",
      "postTransactionBalance": "string"
    }
  ],
  "pageInfo": {
    "previousPage": "string",
    "nextPage": "string"
  }
}
```

<div style="page-break-after: always;"></div>

## Wnioski

Na podstawie analizy przykładowych danych z trzech wybranych banków stwierdzam, że projekt, który chciałbym przeprowadzić, jest możliwy do zrealizowania, a także może być rozwijany w celu obsługi większej liczby banków.
