# Frontend Hızlı Başlangıç

## Adım 1: Bağımlılıkları Yükle

```bash
cd frontend
npm install
```

## Adım 2: Development Server'ı Başlat

```bash
npm run dev
```

## Beklenen Çıktı

Terminal'de şuna benzer bir çıktı görmelisiniz:

```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3001/
  ➜  Network: http://192.168.x.x:3001/
```

## Sorun Giderme

### Port 3001 kullanılıyorsa

Vite otomatik olarak bir sonraki boş portu kullanacaktır. Terminal çıktısındaki gerçek portu kontrol edin.

### "npm: command not found" hatası

Node.js yüklü değil. [Node.js](https://nodejs.org/) yükleyin (v20 veya üzeri).

### Bağımlılık hataları

```bash
rm -rf node_modules package-lock.json
npm install
```

### Port değiştirmek isterseniz

`vite.config.ts` dosyasındaki `port: 3001` değerini değiştirin.

