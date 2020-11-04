// eslint-disable-next-line import/no-named-as-default-member
import APIService from '@/services/api_service';

const ServiceManagerUrl = 'http://localhost:2354';

export default class ServiceManager {
  state = 'IDLE';

  apiService = null;

  constructor() {
    this.apiService = new APIService(ServiceManagerUrl);
  }

  async sendStartRequest(isbnString) {
    console.log('service-manager: sendStartRequest');
    console.log(isbnString);
    const data = await this.apiService.postPlainText(isbnString);
    console.log(data);
    if (data.status === 'finish loading model') {
      console.log(data);
      return true;
    }
    return false;
  }

  async sendSearchText(searchText) {
    console.log('service-manager: sendSearchText');
    const data = await this.apiService.postPlainText(`{"search-text": ${searchText}}`);
    console.log(data);
    // if (data.status === 'finish loading model') {
    //   // this.state = data.state;
    //   // eslint-disable-next-line no-template-curly-in-string
    //   console.log(data);
    // }
  }

  async sendEndRequest() {
    console.log('service-manager: sendEndRequest');
    const data = await this.apiService.postPlainText('{ "command": "EXIT" }');
    console.log(data);
    if (data.status === 'finish search session') {
      console.log(data);
      return true;
    }
    return false;
  }

  async getServerState() {
    console.log('service-manager: getServiceState');
    const data = await this.apiService.get();
    console.log(data);
    if (data.message === 'Manager status') {
      this.state = data.state;
      // eslint-disable-next-line no-template-curly-in-string
      console.log(`data.state: ${this.state}`);
    }
  }

  get state() {
    return this.state;
  }
}
