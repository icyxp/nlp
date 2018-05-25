import App from '../App'
import index from '../pages/index/index'
import result from '../pages/result/result'

export default [
    { path: '/', component: index },
    { path: '/result/:uuid', component: result },
]