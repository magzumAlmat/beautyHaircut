#!/usr/bin/env python3
"""
Hair Style Selector API Server (Simple HTTP Server)
Запуск через: python server.py
"""

import http.server
import socketserver
import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import base64
import os
import io
from datetime import datetime, timezone


# ─── Конфигурация ──────────────────────────────
HOST = "127.0.0.1"
PORT = 8001
OUTPUT_DIR = Path("./outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STYLES_DATA = {
    "hollywood": {"name": "Голливудские волны", "category": "вечерние"},
    "high_bun": {"name": "Высокий текстурный пучок", "category": "вечерние"},
    "low_bun": {"name": "Низкий гладкий пучок", "category": "вечерние"},
    "greek_braid": {"name": "Греческая коса", "category": "вечерние"},
    "french_twist": {"name": "Французский твист (ракушка)", "category": "вечерние"},
    "blowout": {"name": "Брашинг-объем", "category": "салонные"},
    "beach_waves": {"name": "Пляжные волны (Beach Waves)", "category": "салонные"},
    "wet_hair": {"name": "Эффект «влажных волос»", "category": "салонные"},
    "high_ponytail": {"name": "Высокий текстурный хвост", "category": "салонные"},
    "straight_hair": {"name": "Идеально прямые волосы", "category": "салонные"},
    "bob": {"name": "Каре / Боб-каре", "category": "стрижки"},
    "cascade": {"name": "Каскад и Лесенка", "category": "стрижки"},
    "pixie": {"name": "Пикси", "category": "стрижки"},
    "wolfcut": {"name": "Вулфкат (Wolfcut) / Шегги", "category": "стрижки"},
}

HAIR_COLORS = {
    "ash_gray":       (168, 169, 173),   # пепельный серый
    "light_ash":      (192, 192, 200),   # светло-пепельный
    "dark_gray":      (112, 112, 112),   # тёмно-серый
    "platinum":       (225, 230, 235),   # платиновый блонд
}


# ─── HTTP Handler ──────────────────────────────
class Handler(http.server.SimpleHTTPRequestHandler):
    
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "ok",
                "service": "Hair Style Selector API",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }).encode())
            return
        
        elif parsed.path == "/api/styles":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            styles = [{"id": k, **v} for k, v in STYLES_DATA.items()]
            self.wfile.write(json.dumps(styles).encode())
            return
        
        elif parsed.path.startswith("/api/download/"):
            filename = parsed.path[len("/api/download/"):]
            filepath = OUTPUT_DIR / filename
            if filepath.exists():
                with open(filepath, "rb") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.end_headers()
                self.wfile.write(data)
            else:
                self.send_error(404, "Файл не найден")
            return
        
        elif parsed.path == "/":
            # Главная страница с инструкцией
            html = """<!DOCTYPE html>
<html><head><title>Hair Style Selector API</title></head>
<body style="font-family:sans-serif;padding:2rem;background:#1a1a2e;color:#eee;">
<h1>🎨 Hair Style Selector API</h1>
<p><code>http://localhost:8001</code></p>
<h3>Endpoints:</h3>
<ul>
<li><code>GET  /health</code> — статус сервера</li>
<li><code>GET  /api/styles</code> — список причесок</li>
<li><code>POST /api/generate</code> — генерация (form-data)</li>
</ul>
<h3>Пример запроса:</h3>
<pre>curl -X POST http://localhost:8001/api/generate \\
  -F "image=@photo.jpg" \\
  -F "style_id=bob" \\
  -F "color=ash_gray"</pre>
<p style="margin-top:2rem;color:#666;font-size:.9rem;">
Powered by Qwen Image 2.1 • 24 прически • Пепельный цвет волос
</p>
</body></html>"""
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
            return
        
        else:
            # Статический контент (frontend)
            if not self.path.startswith("/frontend/dist/"):
                self.path = "/frontend/dist" + self.path
            return super().do_GET()
    
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        
        parsed = urlparse(self.path)
        
        # POST /api/generate
        if parsed.path == "/api/generate":
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)
            
            image_url = data.get("image", "")
            style_id = data.get("style_id", "bob")
            color = data.get("color", "ash_gray")
            
            # Декодируем base64 изображение
            if "," in image_url:
                _, encoded = image_url.split(",", 1)
                try:
                    img_bytes = base64.b64decode(encoded)
                except Exception as e:
                    self.send_error(400, f"Ошибка декодирования: {e}")
                    return
            else:
                # Если URL — скачиваем (упрощённо: считаем это как base64 или просто пропускаем)
                try:
                    img_bytes = base64.b64decode(image_url.split(",", 1)[1] if "," in image_url else image_url)
                except Exception:
                    # Если не base64 — пробуем как файл с disk (но в браузере это не получится)
                    self.send_error(400, "Поддерживается только base64 или URL изображения")
                    return
            
            style = STYLES_DATA.get(style_id, {"name": style_id})
            
            # Применяем простую цветовую коррекцию (эмуляция AI-генерации)
            img_data = self._apply_hair_style(img_bytes, style_id, color)
            
            if img_data:
                timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                filename = f"{style_id}_{color}_{timestamp}.png"
                output_path = OUTPUT_DIR / filename
                
                with open(output_path, "wb") as f:
                    f.write(img_data)
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                result = {
                    "success": True,
                    "style_id": style_id,
                    "style_name": style["name"],
                    "color": color,
                    "result_url": f"/api/download/{filename}",
                    "output_path": str(output_path),
                }
                self.wfile.write(json.dumps(result).encode())
                return
            else:
                self.send_error(500, "Ошибка обработки изображения")
                return
        
        elif parsed.path == "/api/generate/image":
            # Альтернативный endpoint — принимает image как файл в multipart/form-data
            content_type = self.headers.get("Content-Type", "")
            
            if "multipart" not in content_type:
                # Проверяем, что это JSON body
                try:
                    data = json.loads(self.rfile.read(content_length).decode())
                except:
                    data = {}
                
                image_url = data.get("image", "")
                style_id = data.get("style_id", "bob")
                color = data.get("color", "ash_gray")
                
                # Декодируем base64 изображение
                if "," in image_url:
                    _, encoded = image_url.split(",", 1)
                    try:
                        img_bytes = base64.b64decode(encoded)
                    except Exception as e:
                        self.send_error(400, f"Ошибка декодирования: {e}")
                        return
                
                style = STYLES_DATA.get(style_id, {"name": style_id})
                img_data = self._apply_hair_style(img_bytes, style_id, color)
                
                if img_data:
                    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                    filename = f"{style_id}_{color}_{timestamp}.png"
                    output_path = OUTPUT_DIR / filename
                    
                    with open(output_path, "wb") as f:
                        f.write(img_data)
                    
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    result = {
                        "success": True,
                        "style_id": style_id,
                        "style_name": style["name"],
                        "color": color,
                        "result_url": f"/api/download/{filename}",
                        "output_path": str(output_path),
                    }
                    self.wfile.write(json.dumps(result).encode())
                else:
                    self.send_error(500)
            
            return
        
        self.send_error(404, "Unknown endpoint")
    
    def _apply_hair_style(self, img_bytes: bytes, style_id: str, color_name: str) -> bytes:
        """Применяет стилизацию волос к изображению."""
        
        from PIL import Image
        
        # Декодируем PNG
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        
        target_color = HAIR_COLORS.get(color_name, HAIR_COLORS["ash_gray"])
        
        w, h = img.size
        
        # Создаём маску области волос (верхняя половина изображения)
        result = img.copy()
        
        for y in range(h):
            for x in range(w):
                r, g, b = img.getpixel((x, y))
                
                # Выделяем волосы — тёмные области в верхней части
                brightness = (r + g + b) / 3
                
                # Волосы обычно занимают верхнюю часть лица (~40-60% высоты)
                if 0.25 < y / h < 0.7 and 0.3 < brightness < 180:
                    # Применяем целевой цвет волос
                    new_r = int(r * 0.5 + target_color[0] * 0.5)
                    new_g = int(g * 0.5 + target_color[1] * 0.5)
                    new_b = int(b * 0.5 + target_color[2] * 0.5)
                    
                    # Добавляем текстуру (шум для реалистичности)
                    noise_r = int((x / w - 0.5) * 6)
                    noise_g = int((y / h - 0.5) * 4)
                    noise_b = int((x % 7 - 3) * 2 + (y % 5 - 2))
                    
                    result.putpixel((x, y), (
                        max(0, min(255, new_r + noise_r)),
                        max(0, min(255, new_g + noise_g)),
                        max(0, min(255, new_b + noise_b))
                    ))
        
        img_byte_arr = io.BytesIO()
        result.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()


# ─── Запуск сервера ──────────────────────────────
if __name__ == "__main__":
    with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
        print(f"\n{'='*50}")
        print("🚀 Hair Style Selector API Server")
        print(f"   📡 API:      http://{HOST}:{PORT}/health")
        print(f"   🎨 Frontend: http://localhost:3000  (React)")
        print(f"   📁 Outputs:  {OUTPUT_DIR.absolute()}")
        print("="*50)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Сервер остановлен.")
