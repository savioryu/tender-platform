import { Controller, Get, Param, Post, Body } from '@nestjs/common';
import { AnnouncementService } from './announcement.service';

@Controller('announcement')
export class AnnouncementController {
  constructor(private announcementService: AnnouncementService) {}
  @Get('getDetail/:id')
  async getDetail(@Param('id') id: string): Promise<any> {
    const data = await this.announcementService.getDetail(id);
    return { code: 0, msg: 'ok', data };
  }
  @Post('getList')
  async getAnnouncementsPost(
    @Body() req: { page: number; limit: number; purchaser_name: string },
  ): Promise<any> {
    const { page, limit, purchaser_name } = req;
    const data = await this.announcementService.getAnnouncements(
      page,
      limit,
      purchaser_name,
    );
    return { code: 0, msg: 'ok', data };
  }
  @Post('updateField')
  async updateOrCreateField(
    @Body()
    body: {
      contentId: string;
      fieldName: string;
      newFieldValue: string | boolean;
    },
  ): Promise<any> {
    try {
      const { contentId, fieldName, newFieldValue } = body;
      const updatedDocument =
        await this.announcementService.updateOrCreateField(
          contentId,
          fieldName,
          newFieldValue,
        );

      if (updatedDocument) {
        return {
          code: 0,
          message: 'Field updated or created successfully',
        };
      } else {
        return { code: 50001, message: 'Failed to update or create field' };
      }
    } catch (error) {
      return { error: 'An error occurred', message: error.message };
    }
  }
}
