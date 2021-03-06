/* eslint-disable no-restricted-syntax */
<template>
  <div class="home">
    <b-container class="user-name-header">
      <div>
        <b-card border-variant="light" :header="cardHeaderUserName" align="center">
          <b-card-text v-if='isDisplayUserInfo'>
            <b>Genres, Categories and Topics:</b>
            {{interestedCategories}}
          </b-card-text>
        </b-card>
      </div>
    </b-container>
    <div class="mb-3">
      <b-button :disabled='isDisableUserSelection' v-b-toggle.user-selection-sidebar class="mr-1">
        Select User
      </b-button>
      <b-button :disabled='!isDisplayUserInfo' v-b-toggle.user-borrowing-history class="mr-1">
        Borrowing History
      </b-button>
      <b-button @click="userkeyFuntion()"
                :disabled='isDisableUserkeyFunction'
                class="mr-1">
        <div v-if="isLoading">
          <b-spinner small type="grow"></b-spinner>
          {{userkey}}
        </div>
        <div v-else>
          {{userkey}}
        </div>
      </b-button>
    </div>
    <b-container>
      <b-collapse id="user-borrowing-history">
        <b-card title="User Borrowing History">
          <div>
            <b-table striped hover :items="borrowingHistroy" class="text-left"></b-table>
          </div>
        </b-card>
      </b-collapse>
    </b-container>

    <b-sidebar id="user-selection-sidebar" title="Select a Library User" shadow>
      <div class="px-3 py-2">
        <div>
          <b-form-select v-model="userName"
                        class="mb-3"
                        :options="nameList"
                        :disabled='isDisableUserSelection'
                        @change="setUser($event)">
            <template #first>
              <b-form-select-option :value="null" disabled>
                -- Please select a user --
              </b-form-select-option>
            </template>
          </b-form-select>
        </div>
      </div>
    </b-sidebar>

    <b-container>
      <b-row>
        <b-col>
        </b-col>
        <b-col cols="6">
          <b-input-group size="md" class="mb-3">
            <b-input-group-prepend is-text>
              <b-icon icon="search"></b-icon>
            </b-input-group-prepend>
            <b-form-input v-model="searchText"
                          type="search"
                          placeholder="Search Book Titles"
                          :disabled='isDisableSearch'
                          class="mr-1">
            </b-form-input>
            <b-button @click="searchBookTitle(searchText)"
                      :disabled='isDisableSearch'>
                      Search
            </b-button>
          </b-input-group>
        </b-col>
        <b-col>
        </b-col>
      </b-row>
    </b-container>

    <b-container v-if="recommendedBooks!=null">
      <b-card title="Recommended Books">
        <div>
          <b-table striped hover :items="recommendedBooks" class="text-left"></b-table>
        </div>
      </b-card>
    </b-container>
  </div>
</template>

<script>
import userData from '@/data/user_data';
import ServiceManager from '@/service_manager/service_manager';

export default {
  name: 'Home',
  data() {
    return {
      userName: null,
      userId: null,
      searchText: '',
      searchState: 'IDLE',
      serviceManager: null,
      serviceManagerAddress: null,
      userkeyText: 'Load User Profile',
      recommendedBooks: null,
    };
  },
  computed: {
    borrowingHistroy() {
      if (this.userId === null) return null;
      return userData[this.userId].borrowingHistory;
    },
    nameList: () => userData.map((a) => a.name),
    cardHeaderUserName() {
      if (this.userId === null) return null;
      return `Current User: ${userData[this.userId].name}`;
    },
    interestedCategories() {
      if (this.userId === null) return null;
      const cat = [];
      // eslint-disable-next-line no-restricted-syntax
      for (const book of userData[this.userId].borrowingHistory) {
        this.addNonEmptyStringToArray(cat, book.genre);
        this.addNonEmptyStringToArray(cat, book.topical_main);
        this.addNonEmptyStringToArray(cat, book.topical_geographical);
      }
      return [...new Set(cat)].join(', ');
    },
    isDisableUserSelection() {
      return this.searchState !== 'IDLE';
    },
    isDisplayUserInfo() {
      return this.userName !== null;
    },
    isDisableUserkeyFunction() {
      return (this.searchState === 'LOADING' || this.userName == null);
    },
    isDisableSearch() {
      return this.searchState !== 'READY';
    },
    isLoading() {
      return this.searchState === 'LOADING';
    },
    userkey() {
      // eslint-disable-next-line no-nested-ternary
      return (this.searchState === 'READY') ? 'End Session'
        : (this.searchState === 'IDLE') ? 'Load User Profile' : 'Loading...';
    },
  },
  methods: {
    addNonEmptyStringToArray(a, s) {
      if (s.length > 0) {
        a.push(...s.split(','));
      }
    },
    setUser(event) {
      this.userId = this.nameList.indexOf(event);
    },
    getIsbnString() {
      return JSON.stringify(this.borrowingHistroy.map((a) => a.ISBN));
    },
    async searchBookTitle(searchText) {
      // assume that when serviceManage is not instanciated, this function will not be called
      console.log(`search: ${searchText}`);
      const recommendedBooks = await this.serviceManager.sendSearchText(searchText);
      this.recommendedBooks = JSON.parse(recommendedBooks);
    },
    async userkeyFuntion() {
      await this.serviceManager.getServerState();
      this.searchState = this.serviceManager.state;
      console.log(`searchState = ${this.searchState}`);

      switch (this.searchState) {
        case 'IDLE':
          {
            this.searchState = 'LOADING';
            const success = await this.serviceManager.sendStartRequest(this.getIsbnString());
            console.log(`Home - IDLE: start session response ${success}`);
            this.searchState = success ? 'READY' : 'IDLE';
          }
          break;

        case 'READY':
          {
            this.searchState = 'LOADING';
            const success = await this.serviceManager.sendEndRequest();
            console.log(`Home - READY: end session response ${success}`);
            this.searchState = success ? 'IDLE' : 'READY';
          }
          break;

        default:
          break;
      }
    },
  },
  mounted() {
    // eslint-disable-next-line no-undef
    this.serviceManagerAddress = config.SERVICE_MANAGER_ADDRESS;
    this.serviceManager = new ServiceManager(this.serviceManagerAddress);
  },
};
</script>
