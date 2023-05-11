import PropTypes from 'prop-types'
import Comments from './Comments'

export default function Postcard({ post }) {

  return (
    <>
        <div className="border-2 m-1 border-zinc-400 text-moonlight p-1 rounded-md hover:text-moonlight hover:border-moonlight mt-3">
                <a href="">
                <div className="grid grid-col-2">
                    <div className="col-span-2">
                        Here
                    </div>
                    <div className="col-span-10">
                        <div className="text-xl text-left">
                            <h1>{ post.title }</h1>
                        </div>
                        <div className=" text-left">
                            <h1>{ post.description }</h1>
                        </div>
                    </div>
                </div>
                </a>
            <Comments />
        </div>
    </>
  )
}

Postcard.propTypes = {
  post: PropTypes.string
}

// 'midnight': '#091123',
// 'afterhour':'#212A3E',
// 'moonlight':'#F1F6F9',
// 'regal': '#34172D',
// 'lining':'#d678a4',