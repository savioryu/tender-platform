/* announcement.schema.ts */
import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';
export type AnnouncementDocument = Announcement & Document;

// 当你指定集合名称为 'tender_purchase_list' 时，Mongoose 会自动将其复数化为 'tender_purchase_lists'。
// 这是 Mongoose 的默认行为，旨在遵循常见的命名约定。如果想覆盖这个行为，可以通过在 @Schema() 装饰器中传递 collection 参数来实现。
// 通过 mongoose 更新的字段需要在 schema 中定义
@Schema({ collection: 'tender_purchase_list' })
export class Announcement extends Document {
  @Prop()
  _id: string;
  @Prop()
  contentId: string;
  @Prop()
  title: string;
  @Prop()
  budget: string;
  @Prop({ default: false })
  need_refresh: boolean;
}
export const AnnouncementSchema = SchemaFactory.createForClass(Announcement);

AnnouncementSchema.index({ releaseTime: -1 });
