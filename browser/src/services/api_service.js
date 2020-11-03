import axios from 'axios';

export default class APIService {
  API_URL = '';

  constructor(apiAddress) {
    this.API_URL = apiAddress;
  }

  async get() {
    console.log('ApiService: get()');
    const response = await axios.get(this.API_URL);
    console.log(`ApiService: get result: ${response.data}`);
    return response.data;
  }

  async post(params) {
    const response = await axios.post(this.API_URL, params);
    return response.data;
  }
}
