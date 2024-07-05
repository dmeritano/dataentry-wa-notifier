# WhatsApp Notifier For:
## DATA ENTRY Activities Like:
#### DocumentsReview (v6) - FactoryWebActiviy (v5) - Other

**Current versión**: 1.0

**Description:** This application notifies data-entry operators, via WhatsApp messages, about how many documents are pending review in each activity(*).

(*) Refers to configured activities or sets of documents stored in an Addalia DMS repository (versions 5 or 6).

The retrieval of the number of documents and other interactions with the DMS is done through the DmsRestService (DMS Query Language).

Query results are sent to the configured recipients (phone numbers) using the WhatsApp API.  

**Configuration File:** ```appconfig.json```

**Sample:**
```json
{
    "wappAuthToken": "[whatsapp-token]",
    "wappApiUrl": "https://graph.facebook.com/v19.0/[Identificador-del-numero-de-telefono-origen]/messages",
    "jobs": [
        {
            "factoryProcess": "Revision Op. Cliente XYZ",
            "description": "Tarea para obtencion pendientes para las Act X y Act Y",
            "dmsUri": "https://[IP-Rest-Service]/RestService",
            "dmsUser": "USUARIO",
            "dmsPass": "PASSWORD",
            "dmsQueries": [
                {
                    "query": "DocumentoRevision$#Queue=1",
                    "queryDescription": "O.C.R."
                },
                {
                    "query": "DocumentoRevision$#Queue=2",
                    "queryDescription": "Completado Datos"
                }
            ],
            "wappTemplate": "[name of a configured whatsapp template]",
            "wappRecipients": [
                "+54111.........",
                "+34408........."
            ],
            "sendMessageWithSameData": true
        }
    ]
}
```

```sendMessageWithSameData``` Indicates whether to send notification to users even when the data sent in the last message has not changed.

### DISTRIBUTION

```build.bat``` located in project root folder use pyinstaller to generate executable (EXE) in the DIST folder of the project. Batch script also copies the configuration file to "DIST"  folder.