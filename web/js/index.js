import {Amplify, API} from 'aws-amplify'
import { config } from './aws-exports'

// yes commit please
Amplify.configure(config)
const getData = async() => {
    const data = await API.get('forestapi', 'api')
    console.log(data)
}
