<template>
  <div class="app-container">
    <div class="filter-container">
      <el-form :inline="true" class="demo-form-inline">
        <el-form-item label="项目名称">
          <el-input v-model="listQuery.title" placeholder="项目名称" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
        </el-form-item>
        <el-form-item label="采购人">
          <el-input v-model="listQuery.purchaser_name" placeholder="采购人" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
        </el-form-item>
        <el-form-item label="代理机构">
          <el-input v-model="listQuery.agency_name" placeholder="代理机构" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
        </el-form-item>
        <el-form-item>
          <el-button class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
            Search
          </el-button>
        </el-form-item>
      </el-form>
    </div>
    <el-table v-loading="listLoading" :data="list" element-loading-text="Loading" border fit highlight-current-row>
      <el-table-column label="项目名称">
        <template slot-scope="scope">
          <el-link type="primary" @click="goDetail(scope.row.contentId)">
            {{ scope.row.title }}
          </el-link>
        </template>
      </el-table-column>
      <el-table-column label="预算金额" width="auto" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.budget }}</span>
        </template>
      </el-table-column>
      <el-table-column label="采购人信息" width="auto" align="center">
        <template slot-scope="scope">
          {{ scope.row.purchaser_name }}
        </template>
      </el-table-column>
      <el-table-column label="采购人代理机构" width="auto" align="center">
        <template slot-scope="scope">
          {{ scope.row.agency_name }}
        </template>
      </el-table-column>
      <el-table-column label="开标时间" width="auto" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.bid_opening_time }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="auto" class-name="small-padding">
        <template slot-scope="scope">
          <el-button type="warning" size="large" :icon="scope.row.need_refresh ? 'el-icon-star-on' : 'el-icon-star-off'" circle @click="handleMarkRefresh(scope.row)" />
        </template>
      </el-table-column>
    </el-table>
    <pagination v-show="total > 0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

  </div>
</template>

<script>
import { getList, updateField } from '@/api/announcement';
import Pagination from '@/components/Pagination';
export default {
  components: { Pagination },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'gray',
        deleted: 'danger'
      };
      return statusMap[status];
    }
  },
  data() {
    return {
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 10,
        title: '',
        purchaser_name: '',
        agency_name: ''
      }
    };
  },
  created() {
    this.getList();
  },
  methods: {
    getList() {
      this.listLoading = true;
      console.log(this.listQuery);
      getList(this.listQuery).then(response => {
        this.list = response.data.items;
        this.total = response.data.total;
        this.listLoading = false;
      });
    },
    goDetail(contentId) {
      // this.$router.push({ path: '/purchase/detail', query: { contentId } });
      const newTab = window.open(`#purchase/detail?contentId=${contentId}`, '_blank');
      newTab.focus();
    },
    handleFilter() {
      this.listQuery.page = 1;
      this.getList();
    },
    handleMarkRefresh(item) {
      const { contentId, need_refresh } = item;
      const need_refresh_new = !need_refresh;
      updateField({ contentId, fieldName: 'need_refresh', newFieldValue: need_refresh_new }).then(res => {
        if (res.code === 0) {
          this.updateList({ contentId, need_refresh: need_refresh_new });
        }
      });
    },
    updateList(updateItem) {
      // 根据实际情况，更新列表中的数据
      const index = this.list.findIndex(item => item.contentId === updateItem.contentId);
      if (index !== -1) {
        this.list[index].need_refresh = updateItem.need_refresh;
      }
    }
  }
};
</script>
