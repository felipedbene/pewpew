# Valores que se pueden sacar

## **total**

### Descripción:

Da el valor total de (?) - _probablemente documentos escaneados_

### Ejemplo

```javascript
"total": 2110664,
```

* * *

## **took**

### Descripción:

Da el valor de (?) - _probablemente amenazas encontradas_

### Ejemplo

```javascript
"took": 488,
```

* * *

## tags

### Ejemplo

```javascript
"commodity.triusor": {
  "support_id": 1,
  "tag_name": "Triusor",
  "public_tag_name": "Commodity.Triusor",
  "tag_definition_scope_id": 3,
  "tag_definition_status_id": 1,
  "count": 119899,
  "lasthit": "2018-10-22 14:45:38",
  "description": "Triusor searches files with .exe extension in the system and infects the files.",
  "customer_name": "Palo Alto Networks Unit42",
  "customer_industry": "High Tech",
  "source": "Unit 42",
  "tag_class_id": 3,
  "tag_definition_id": 67936,
  "tag_groups": [{
    "tag_group_name": "FileInfector",
    "description": "FileInfector related tags"
  }]
}
```

### Descripción

* * *

## **hits**

### Ejemplo

```javascript
"hits": [{
  "_source": {
    "sha1": "4c3e98723fbd762cd46ac7808599df73c25b46cc",
    "filetype": "Android APK",
    "app_name": "System UI",
    "malware": 1,
    "sha256": "ac2135a7577162dd176880ba433fc3ecc949a810033744c7359af1aae83802cd",
    "size": 4086506,
    "finish_date": "2018-10-22T15:02:12",
    "ssdeep": "49152:DOumUQcUj2x+DKm8Xo33WubhHSYoTIXx8OGraDldXWoTIXLgpjVUlxTS5inoz1qj:NUKxJ09bgMdGeK+vd1q2j6rD",
    "region": ["us"],
    "create_date": "2018-10-22T15:00:55",
    "md5": "acdf483f0e22ffd78322a8289f554642",
    "tag": [],
    "tag_groups": []
  },
  "_id": "ac2135a7577162dd176880ba433fc3ecc949a810033744c7359af1aae83802cd",
  "visible": true
}]
```
