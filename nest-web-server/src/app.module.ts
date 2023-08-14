import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { AnnouncementModule } from './announcement/announcement.module';

@Module({
  imports: [
    MongooseModule.forRoot('mongodb://127.0.0.1:27017/tender_purchase'),
    AnnouncementModule,
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
