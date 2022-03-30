# WebCam RGB

Toma fotos cada cierto intervalo

### Test

para pruebas lo mejor es ejecutarlo desde el terminar

```bash
python main.py <interval_sec:int> <path:string>
```

- `interval` cada cuanto se toman fotos, en segundos
- `path` carpeta donde se guiardan las fotos


**importante** detener deamon

```bash
sudo systemctl stop camera_rgb.service
```


### Install as deamon

editar `camera_rgb.service` para configar el intervalo y la carpeta

```bash
# driver
sudo apt install fswebcam

# instalar como un servicio
sudo systemctl link /home/pi/camera_rgb/camera_rgb.service
sudo systemctl daemon-reload
sudo systemctl enable

# iniciar deamon
sudo systemctl start camera_rgb.service
```


### run at specific hours

quizas no se quiera capturas 24/7, para esto lo mejor es configurar [cron](https://blog.desdelinux.net/cron-crontab-explicados/?utm_source=destacado-inside)


inicia la toma de fotos a las 04:00
```
0 4 * * * sudo systemctl start camera_rgb.service
```

detiene la toma de fotos a las 18:00
```
0 18 * * * sudo systemctl stop camera_rgb.service
```

### Backup

para los backup sugiero usar [rclone.org](https://rclone.org), en conjunto con cron

