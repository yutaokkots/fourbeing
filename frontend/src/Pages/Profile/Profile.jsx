import React from 'react'
import Navbar from '../../components/Navbar/Navbar'


export default function Profile() {
  return (
    <>
        <div>
            <Navbar/>
            <div className="mt-16">

                <div className="grid grid-cols-7 gap-5">
                    <div className='bg-moonlight col-start-2 col-span-2'>
                        <div>Profile</div>
                    </div>
                    <div className='bg-regal col-start-4 col-span-3'>

                    </div>
                </div>
            </div>
        </div>
    </>
  )
}
// 'midnight': '#091123',
// 'afterhour':'#212A3E',
// 'moonlight':'#F1F6F9',
// 'regal': '#34172D',
// 'lining':'#d678a4',