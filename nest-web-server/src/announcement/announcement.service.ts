import { Model } from 'mongoose';
import { InjectModel } from '@nestjs/mongoose';
import { Injectable } from '@nestjs/common';
import { AnnouncementDocument } from './announcement.schema';

@Injectable()
export class AnnouncementService {
  // 注册 Schema 后，可以使用 @InjectModel() 装饰器将 Announcement 模型注入到 AnnouncementService 中:
  constructor(
    @InjectModel('tender_purchase_list')
    private announcementModel: Model<AnnouncementDocument>,
  ) {}
  async getDetail(id: string): Promise<any> {
    const detail = await this.announcementModel.find({ contentId: id }).exec();
    return detail;
  }
  async getAnnouncements(
    page: number,
    limit: number,
    purchaser_name: string,
  ): Promise<any> {
    // 筛选条件
    const filters = {
      purchaser_name: { $regex: new RegExp(purchaser_name, 'i') },
    };
    // 字段投影，将要返回的字段设为 1，要排除的字段设为 0
    const projection = {
      txt: 0,
    };
    const skip = (page - 1) * limit;
    const items = await this.announcementModel
      .find(filters, projection)
      .skip(skip)
      .limit(limit)
      .exec();
    const total = await this.announcementModel.countDocuments(filters).exec();
    return { items, total };
  }
}
