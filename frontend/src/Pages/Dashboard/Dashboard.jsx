import { useState, useEffect } from 'react'
import * as postsAPI from '../../utilities/posts_api'
import Navbar from '../../components/Navbar/Navbar'
import Postcard from '../../components/Postcard/Postcard'

export default function Dashboard() {
    const [allPosts, setAllPosts] = useState([""])

    useEffect(() => {
        async function getPosts(){
            try{
                postsAPI.getPost().then((response) => {
                    return response.test
                }).then((response)=>{
                    setAllPosts(response)
                }).catch(error => {
                    throw(error);
                })
            }
            catch(err){
                console.log('err', err)
            }
        }
        getPosts()
    }, [])

    return (
        <>
            <Navbar />
            <div>Dashboard</div>
            <div>
                {allPosts?.map((post, idx) => 
                    <Postcard  post={post} key={idx}/>)
                }
            </div>
        </>

    )
}


