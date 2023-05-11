import { useContext } from 'react'
import { AuthContext } from "../../Pages/App"
import * as userService from "../../utilities/users-service"

export default function Navbar() {
    const { user, setUser } = useContext(AuthContext)

    // let links = [
    //     {name: 'Home', link: '/'},
    //     {name: 'About', link: '/about'},
    //     {name: 'Profile', link: '/profile'},
    //     {name: 'Login', link: '/login'},
    //     {name: 'Logout', link: '/logout'},
    // ]

    function logOut(){
        userService.logOut()
        setUser(null)
    }

    return (
        <>
            <div className="nav shadow-lg w-full fixed top-0 left-0">
                <div className="md:flex items-center justify-between bg-white py-3 md:px-10 px-7">
                    <div className="font-bold text-2xl cursor-pointer flex items-center ">
                    <span><a href="/" className="site-title">Site Name</a></span>
                    <ul className="md:flex md:item-center">
                        {/* {links.map((link, idx) => 
                        <li key={idx} className="md:ml-8 text-xl"> 
                            <a className="text-gray-800 hover:text-gray-400 duration-300" 
                                href={ link.link }>{ link.name }</a>
                        </li>
                        )}  */}
                        <li className="md:ml-8 text-xl">
                            <a className="text-gray-800 hover:text-gray-400 duration-300" 
                                href='/'>Home</a>
                        </li>
                        
                        <li className="md:ml-8 text-xl">
                            <a className="text-gray-800 hover:text-gray-400 duration-300" 
                                href='/profile'>Profile</a>
                        </li>
                        { user &&
                        <li className="md:ml-8 text-xl">
                            <a className="text-gray-800 hover:text-gray-400 duration-300" 
                                href='/profile'>hello, {user}</a>
                        </li>
                        }   
                        <li className="md:ml-8 text-xl">
                            <a className="text-gray-800 hover:text-gray-400 duration-300" 
                                href='/login'>Login</a>
                        </li>
                        <li className="md:ml-8 text-xl">
                            <a className="text-gray-800 hover:text-gray-400 duration-300" 
                                href='/'
                                onClick={ logOut }
                                >Logout</a>
                        </li>
                    </ul>
                    </div>
                </div>
            </div>
        </>
    )
}
