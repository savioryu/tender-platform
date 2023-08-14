<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.purchaser_name" placeholder="采购人" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        Search
      </el-button>
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
    </el-table>
    <pagination v-show="total > 0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

  </div>
</template>

<script>
import { getList } from '@/api/announcement';
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
        purchaser_name: ''
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
      this.getList();
    }
  }
};
</script>
