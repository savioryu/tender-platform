import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { NestExpressApplication } from '@nestjs/platform-express';

import { join } from 'path';

async function bootstrap() {
  const app = await NestFactory.create<NestExpressApplication>(AppModule);

  const corsOptions = {
    origin: '*', // 允许访问的前端应用的地址
    methods: 'GET,POST', // 允许的 HTTP 方法
    allowedHeaders: 'Content-Type,Authorization', // 允许的请求头
    credentials: true, // 允许发送身份验证凭证（如 cookie、HTTP 认证头）
  };

  app.enableCors(corsOptions);
  app.useStaticAssets(join(__dirname, '..', 'public/dist'));

  await app.listen(8000);
}
bootstrap();
