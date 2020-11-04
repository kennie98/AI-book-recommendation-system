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

  async postPlainText(data) {
    console.log(`ApiService: post() - data: ${data}`);
    const response = await axios.post(this.API_URL,
      data,
      {
        headers: {
          'Content-Type': 'text/plain',
          Accept: '*/*',
        },
      });
    return response.data;
  }
}
