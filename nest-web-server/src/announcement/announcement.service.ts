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
  async updateOrCreateField(
    contentId: string,
    fieldName: string,
    newFieldValue: string | boolean,
  ): Promise<AnnouncementDocument | null> {
    try {
      const filter = { contentId };
      const update = {
        $set: { [fieldName]: newFieldValue },
      };
      const options = { new: true }; // new: 布尔值，true 返回更新后的数据，false （默认）返回更新前的数据
      const updatedDocument = await this.announcementModel.findOneAndUpdate(
        filter,
        update,
        options,
      );

      return updatedDocument;
    } catch (error) {
      console.error('An error occurred during update or create:', error);
      throw error;
    }
  }
}
