import { Module } from '@nestjs/common';
import { AnnouncementController } from './announcement.controller';
import { AnnouncementService } from './announcement.service';
import { MongooseModule } from '@nestjs/mongoose';
import { AnnouncementSchema } from './announcement.schema';

@Module({
  imports: [
    MongooseModule.forFeature([
      { name: 'tender_purchase_list', schema: AnnouncementSchema },
    ]),
  ],
  controllers: [AnnouncementController],
  providers: [AnnouncementService],
})
export class AnnouncementModule {}
