import { useState, useEffect, useContext } from 'react'
import * as postsAPI from '../../utilities/posts_api'
import Navbar from '../../components/Navbar/Navbar'
import Postcard from '../../components/Postcard/Postcard'
import { AuthContext } from '../App'

export default function Dashboard() {
    const [allPosts, setAllPosts] = useState([""])
    const { user, setUser } = useContext(AuthContext)

    useEffect(() => {
        async function getPosts(){
            try{
                postsAPI.getPostAll().then((response) => {
                    return response
                }).then((response)=>{
                    setAllPosts(response.data)
                    console.log(response.data)
                }).catch(error => {
                    throw(error);
                })
            }
            catch(err){
                console.log('err', err)
            }
            }
        getPosts()
        console.log(user)
    }, [])

    return (
        <div >
            <Navbar />
            <div  className="bg-afterhour v-screen h-screen">
                
            
                <div className="mt-10 grid grid-cols-12 gap-4 px-5">
                
                    <div className="col-span-7">
                        <div>Dashboard</div>
                        <div className="">
                            {allPosts?.map((post, idx) => 
                                <Postcard  post={post} key={idx}/>)
                            }
                        </div>
                    </div>
                    <div className="col-span-5">
                        <div className="">
                            <h1> second column </h1>
                        </div>
                        {
                        user ? <h2>The user is logged in</h2>    
                        :
                        <h2 className="text-red-800">The user is not set</h2>    
                        }
                    </div>
                </div>
            </div>
        </div>

    )
}
// 'midnight': '#091123',
// 'afterhour':'#212A3E',
// 'moonlight':'#F1F6F9',
// 'regal': '#34172D',
// 'lining':'#d678a4',

