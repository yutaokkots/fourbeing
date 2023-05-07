import React, { useState } from 'react'
import { useEffect } from 'react' 
import * as postsAPI from '../../utilities/posts_api'
import Postcard from '../../components/Postcard/Postcard'

export default function Dashboard() {
    const [allPosts, setAllPosts] = useState([])

    useEffect(() => {
        async function getPosts(){
            console.log("At the Dashboard before the try-catch")
            try{
                console.log("At the Dashboard")
                
                postsAPI.getPost().then((response) => {
                    setAllPosts(response)
                    console.log(response)
                })
                
                const posts = postsAPI.getPost()
                let postList = posts.test
                console.log(postList)
                setAllPosts(postList)
            }
            catch(err){
                console.log('err', err)
            }
        }
        getPosts()
    }, [])

    console.log(allPosts)
    return (
        <>
        <div>Dashboard</div>
        <div>
            {allPosts.map((post, idx) => 
                <Postcard key={idx} post={post}/>)
            }
        </div>
        </>

    )
}


