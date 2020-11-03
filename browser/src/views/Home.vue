/* eslint-disable no-restricted-syntax */
<template>
  <div class="home">
    <b-container class="user-name-header">
      <div>
        <b-card border-variant="light" :header="cardHeaderUserName" align="center">
          <b-card-text><b>Genres, Categories and Topics:</b> {{interestedCategories}}</b-card-text>
        </b-card>
      </div>
    </b-container>
    <div class="mb-3">
      <b-button :disabled='isDisableUserSelection' v-b-toggle.user-selection-sidebar class="mr-1">
        Select User
      </b-button>
      <b-button v-b-toggle.user-borrowing-history class="mr-1">
        Borrowing History
      </b-button>
      <b-button @click="loadUserProfile()" :disabled='isDisableUserProfileLoad' class="mr-1">
        Load User Profile
      </b-button>
    </div>

    <b-container>
      <b-collapse id="user-borrowing-history">
        <b-card title="User Borrowing History">
          <div>
            <b-table striped hover :items="borrowingHistroy"></b-table>
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
                          class="mr-1">
            </b-form-input>
            <b-button @click="searchBookTitle(searchText)">Search</b-button>
          </b-input-group>
        </b-col>
        <b-col>
        </b-col>
      </b-row>
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
    isDisableUserProfileLoad() {
      return this.userName === null;
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
    searchBookTitle(searchText) {
      console.log(`search: ${searchText}`);
    },
    async loadUserProfile() {
      this.serviceManager = new ServiceManager();
      await this.serviceManager.getServerState();
      this.searchState = this.serviceManager.state;
      console.log(`Home - loadUserProfile = ${this.serviceManager.state}`);
    },
  },
};
</script>
