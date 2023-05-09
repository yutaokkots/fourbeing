import { useState, useEffect } from 'react'
import * as postsAPI from '../../utilities/posts_api'
import Navbar from '../../components/Navbar/Navbar'
import Postcard from '../../components/Postcard/Postcard'

export default function Dashboard({ user }) {
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
            {
            user ? <h2>The user is logged in</h2>    
            :
            <h2 className="text-red-800">The user is not set</h2>    
            }
        </>

    )
}


