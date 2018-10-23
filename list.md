# Valores que se pueden sacar

## **total**

```javascript
"total": 2110664, // Total de archivos escaneados
```

* * *

## **took**

```javascript
"took": 488, // Total de vulnerabilidades encontradas
```

* * *

## tags

```javascript
"tags": {
  "unit42.http_no_user_agent": { // Nombre del programa
    // "support_id": 1,
    "tag_name": "HttpNoUserAgent", // Nombre del programa
    "public_tag_name": "Unit42.HttpNoUserAgent", // Nombre Único del programa
    // "tag_definition_scope_id": 4,
    // "tag_definition_status_id": 1,
    "count": 7827743, // Cuántos archivos infectados
    "lasthit": "2018-10-09 14:07:17", // Hora y fecha del último ataque
    "description": "A sample creates HTTP traffic but omits or uses a blank user-agent field. Typically, legitimate applications will include a user-agent value in HTTP requests. HTTP requests without the user-agent header or with a blank user agent value are extremely suspect. This tag identified such suspect applications.", //Descripción del ataque (sirve para conscientización)
    "customer_name": "Palo Alto Networks Unit42", // A quién atacó (puede ser información sensible)
    "customer_industry": "High Tech", // Categoría del atacado
    "source": "Unit 42", // De donde proviene el ataque
    // "tag_class_id": 5,
    // "tag_definition_id": 41533
  }
}
```

* * *

## **hits**

```javascript
"hits": [{
  "_source": { // Identificador numérico (0..n)
    // "sha1": "0562d8cfc34ef3f49e203700f67fc7ddda76f105",
    "app_packagename": "com.bigpinwheel.game.majiang", // Nombre único del programa
    "filetype": "Android APK", // Categoría
    "app_name": "风扯血战麻将", // Cómo aparece el programa al usuário
    "malware": 1, // Indica si es malware
    // "sha256": "94e5594dc107baa3e3da796cc57003b901392be91de5cc0a0a90445e6b5fbe22",
    "size": 5471129, // Tamaño del archivo
    "finish_date": "2018-10-22T15:01:57", // Fecha de término (?)
    // "ssdeep": "98304:RrdlpH3FTyEhqE53TLpKcEgY9ACE7uWZmKRia/FrMR7//jIU:7nH3EEndIcPyKmKJ/FrMR7DIU",
    "create_date": "2018-10-22T14:57:55", // Fecha de creación (?)
    "region": ["us"], // Regiones (?)
    // "md5": "cb23db8d1d3eaf0c06a1f72b68efca24",
    "tag": ["Unit42.AndroidSudo", "Unit42.AndroidPorn", // Sub-categorías "Commodity.UmengAdware"],
    "tag_groups": ["Android", "AdWare"] //Clasificaciones
  },
  "_id": "94e5594dc107baa3e3da796cc57003b901392be91de5cc0a0a90445e6b5fbe22", // Identificador único
  "visible": true // ??
}]
```
